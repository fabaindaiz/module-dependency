import logging
from collections import deque
from dataclasses import dataclass, field
from typing import Iterable, Optional
from dependency.core.injection.injection import ContainerInjection, ProviderInjection
from dependency.core.injection.mixin import ContainerMixin
from dependency.core.exceptions import ResolutionError
_logger = logging.getLogger("dependency.loader")


@dataclass
class ResolutionNode:
    """A provider being tracked through the expansion BFS.

    Attributes:
        provider: The injection node being processed.
        context: The nearest parent ContainerInjection (from the importer).
        imported_by: Backpointer to the node that first imported this one.
    """
    provider: ProviderInjection
    context: Optional[ContainerInjection]
    imported_by: Optional['ResolutionNode'] = field(default=None, repr=False)

    def import_chain(self) -> list[ProviderInjection]:
        """Return the import path from the root seed down to this node."""
        chain: list[ProviderInjection] = []
        node: Optional[ResolutionNode] = self
        while node is not None:
            chain.append(node.provider)
            node = node.imported_by
        chain.reverse()
        return chain


@dataclass
class ExpansionFailure:
    """A provider that failed to enter the resolution process.

    Attributes:
        node: The resolution node, with import_chain() for backtracing.
        reason: Human-readable explanation of why this provider failed.
    """
    node: ResolutionNode
    reason: str


@dataclass
class ExpansionResult:
    """Result of a ProviderExpansion run.

    Attributes:
        resolved: Providers that successfully entered the injection process.
        failures: Providers that could not enter, with reasons and import chains.
    """
    resolved: set[ProviderInjection]
    failures: list[ExpansionFailure]

    def raise_if_failed(self) -> None:
        """Raise ResolutionError if any failures exist, with full diagnostics."""
        if not self.failures:
            return
        lines = ["Provider expansion failed:"]
        for failure in self.failures:
            chain = failure.node.import_chain()
            if len(chain) > 1:
                chain_str = " → ".join(str(p) for p in chain)
                lines.append(f"  {failure.reason} (imported via: {chain_str})")
            else:
                lines.append(f"  {failure.reason}")
        raise ResolutionError("\n".join(lines))


class ProviderExpansion:
    """Expands the provider dependency graph starting from declared implementations.

    Resolves the tree in three ordered steps:

    1. Seed — implemented providers from the structural tree (declared via
       @module(provides=) or @component(module=)) plus any extras.

    2. Expansion — BFS through imports and optional_imports, discovering
       undeclared providers. Each undeclared provider is placed in the container
       of the provider that first imports it.

    3. Conditions applied during expansion:
       - Required import + no implementation + strict_resolution=True  → ExpansionFailure
       - Required import + no implementation + strict_resolution=False → skipped
       - Optional import + no implementation → silently skipped (never a failure)

    4. Cascade — after BFS, any provider with a failed required import is also
       marked as failed. Optional import failures never cascade.

    Returns an ExpansionResult with both resolved and failed providers.
    Call result.raise_if_failed() to raise ResolutionError on hard failures.
    """

    def __init__(self,
        modules: Iterable[type[ContainerMixin]],
        extra: Iterable[ProviderInjection] = (),
    ) -> None:
        self._modules: list[type[ContainerMixin]] = list(modules)
        self._extra: list[ProviderInjection] = list(extra)

    def expand(self) -> ExpansionResult:
        """Run the full expansion and return resolved + failed providers."""
        nodes: dict[ProviderInjection, ResolutionNode] = {}
        failures: list[ExpansionFailure] = []
        queue: deque[ResolutionNode] = deque()

        self._seed(queue, nodes)

        while queue:
            node = queue.popleft()

            try:
                self._adopt_if_orphan(node.provider, node.context)
            except ResolutionError as e:
                failures.append(ExpansionFailure(node=node, reason=str(e)))
                nodes.pop(node.provider, None)
                continue

            self._enqueue_imports(node, queue, nodes, failures)

        self._cascade_failures(nodes, failures)

        return ExpansionResult(resolved=set(nodes.keys()), failures=failures)

    def _seed(self,
        queue: deque[ResolutionNode],
        nodes: dict[ProviderInjection, ResolutionNode],
    ) -> None:
        """Step 1: add implemented structural providers and extra seeds."""
        for module in self._modules:
            for provider in module.collect_providers():
                if provider.injectable.implementation is not None:
                    node = ResolutionNode(provider=provider, context=None)
                    nodes[provider] = node
                    queue.append(node)
        for provider in self._extra:
            if provider not in nodes:
                node = ResolutionNode(provider=provider, context=None)
                nodes[provider] = node
                queue.append(node)

    def _adopt_if_orphan(self,
        provider: ProviderInjection,
        context: Optional[ContainerInjection],
    ) -> None:
        """Step 2: place undeclared providers near their first importer."""
        if provider.parent is not None or provider.is_root:
            return
        if context is None:
            raise ResolutionError(
                f"Provider {provider} has no parent module and no importer context. "
                f"Declare it with module= or add it to a module via provides=."
            )
        _logger.debug(f"Provider {provider} undeclared, assigning to {context}")
        provider.change_parent(context)
        provider.attach(container=context.container)

    def _enqueue_imports(self,
        node: ResolutionNode,
        queue: deque[ResolutionNode],
        nodes: dict[ProviderInjection, ResolutionNode],
        failures: list[ExpansionFailure],
    ) -> None:
        """Step 3: follow required and optional imports with different conditions."""
        for imported in node.provider.imports:
            if imported in nodes:
                continue
            if imported.injectable.implementation is None:
                if imported.strict_resolution:
                    failures.append(ExpansionFailure(
                        node=ResolutionNode(
                            provider=imported,
                            context=node.context,
                            imported_by=node,
                        ),
                        reason=f"Provider {imported} has no implementation",
                    ))
                else:
                    _logger.warning(f"Provider {imported} has no implementation, skipping")
                continue
            child = ResolutionNode(
                provider=imported,
                context=node.provider.parent,
                imported_by=node,
            )
            nodes[imported] = child
            queue.append(child)

        for imported in node.provider.optional_imports:
            if imported in nodes:
                continue
            if imported.injectable.implementation is None:
                _logger.debug(f"Optional provider {imported} has no implementation, skipping")
                continue
            child = ResolutionNode(
                provider=imported,
                context=node.provider.parent,
                imported_by=node,
            )
            nodes[imported] = child
            queue.append(child)

    def _cascade_failures(self,
        nodes: dict[ProviderInjection, ResolutionNode],
        failures: list[ExpansionFailure],
    ) -> None:
        """Step 4: propagate failures to providers that strictly depend on them.

        Providers with partial_resolution=True are immune — they can operate
        without all their declared imports.
        """
        failed_set: set[ProviderInjection] = {f.node.provider for f in failures}

        changed = True
        while changed:
            changed = False
            to_fail: list[tuple[ProviderInjection, ResolutionNode, ProviderInjection]] = []

            for provider, node in nodes.items():
                for imported in provider.imports:  # only required imports cascade
                    if imported in failed_set:
                        to_fail.append((provider, node, imported))
                        break

            for provider, node, cause in to_fail:
                nodes.pop(provider)
                failed_set.add(provider)
                failures.append(ExpansionFailure(
                    node=node,
                    reason=f"Provider {provider} has unresolvable dependency: {cause}",
                ))
                changed = True
