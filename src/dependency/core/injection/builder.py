"""Materialise an `ApplicationGraph` from the frozen declarations on the classes.

Two phases, and the split is the example application's documented three-step startup:

1. `structure()` builds the container tree from `ModuleSpec`. This is what
   `Entrypoint.__init__` needs, before any implementation has been imported.
2. `bind()` creates a provider node per component and binds exactly one implementation to
   each. This runs after the `imports.py` modules have been imported, which is precisely
   what makes that import the statement of *which implementations this build uses*.

**Discovery costs nothing and keeps no registry.** Every declared module is a subclass of
`ContainerMixin` and every declared component is a subclass of `ProviderMixin`, so Python's
own subclass links are the index. A class that was never imported has no subclass entry and
is correctly invisible — which is exactly what an `imports.py` is for.
"""

from typing import Iterable, Optional
from dependency.core.injection.graph import ApplicationGraph
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.injection import ContainerInjection, ProviderInjection
from dependency.core.injection.mixin import ContainerMixin, ProviderMixin
from dependency.core.injection.spec import (
    ComponentSpec,
    ImplementationSpec,
    own_component_spec,
    own_implementation_spec,
    own_module_spec,
)
from dependency.core.exceptions import DeclarationError


def _descendants(base: type) -> list[type]:
    """Every transitive subclass of `base` that has been imported, depth first."""
    seen: set[int] = set()
    found: list[type] = []
    pending: list[type] = list(base.__subclasses__())
    while pending:
        candidate = pending.pop()
        if id(candidate) in seen:
            continue
        seen.add(id(candidate))
        found.append(candidate)
        pending.extend(candidate.__subclasses__())
    return found


class GraphBuilder:
    """Builds one `ApplicationGraph` from whatever has been declared and imported."""

    def __init__(self, roots: Iterable[type]) -> None:
        """
        Args:
            roots: The `Plugin` classes this application is built from.
        """
        self._roots: tuple[type, ...] = tuple(roots)

    def build(self) -> ApplicationGraph:
        """Structure and bind in one call, for callers with nothing to import between."""
        graph = self.structure()
        self.bind(graph)
        return graph

    def structure(self) -> ApplicationGraph:
        """Build the container tree. No component node exists yet."""
        containers: dict[type, ContainerInjection] = {}
        for module_cls in _descendants(ContainerMixin):
            spec = own_module_spec(module_cls)
            if spec is not None:
                node = ContainerInjection(name=spec.name)
                node.is_root = spec.is_root
                containers[module_cls] = node

        for module_cls, node in containers.items():
            spec = own_module_spec(module_cls)
            if spec is not None and spec.parent is not None:
                parent = containers.get(spec.parent)
                if parent is None:
                    raise DeclarationError(
                        f"Module {spec.name} declares parent {spec.parent.__name__}, which "
                        f"was never declared with @module."
                    )
                node.change_parent(parent)

        missing = [root.__name__ for root in self._roots if root not in containers]
        if missing:
            raise DeclarationError(
                f"Not a declared module: {', '.join(missing)}. A plugin passed to the "
                f"application must carry @module."
            )
        roots = tuple(containers[root] for root in self._roots)
        return ApplicationGraph(roots=roots, containers=containers, nodes={})

    def bind(self, graph: ApplicationGraph) -> None:
        """Create a node per reachable component and bind exactly one implementation to each.

        Reachable means: declared under one of this build's roots, or imported — directly or
        transitively — by something that is. A component declared elsewhere in the process is
        not this application's business, and building a node for it would make every
        declaration anywhere a participant in every build.
        """
        components: dict[type, ComponentSpec] = {}
        for component_cls in _descendants(ProviderMixin):
            spec = own_component_spec(component_cls)
            if spec is not None:
                components[component_cls] = spec

        implementations: dict[type, list[ImplementationSpec]] = {}
        for implementation_cls in _descendants(ProviderMixin):
            implementation = own_implementation_spec(implementation_cls)
            if implementation is not None:
                implementations.setdefault(implementation.target, []).append(
                    implementation
                )

        reachable = self._reachable(graph, components, implementations)

        for component_cls in reachable:
            spec = components[component_cls]
            graph.add_node(
                component_cls,
                ProviderInjection(
                    name=spec.name,
                    injectable=Injectable(interface_cls=component_cls),
                    parent=self._parent_of(graph, component_cls, spec),
                ),
            )

        for component_cls in reachable:
            self._bind_one(
                graph,
                component_cls,
                components[component_cls],
                implementations.get(component_cls, []),
            )

    def _reachable(
        self,
        graph: ApplicationGraph,
        components: dict[type, ComponentSpec],
        implementations: dict[type, list[ImplementationSpec]],
    ) -> list[type]:
        """Components declared under this build's roots, plus their import closure."""
        subtree: set[int] = set()
        pending_containers: list[ContainerInjection] = list(graph.roots)
        while pending_containers:
            container = pending_containers.pop()
            if id(container) in subtree:
                continue
            subtree.add(id(container))
            for child in container.childs:
                if isinstance(child, ContainerInjection):
                    pending_containers.append(child)

        def declared_here(component_cls: type, spec: ComponentSpec) -> bool:
            parent = self._parent_of(graph, component_cls, spec)
            return parent is not None and id(parent) in subtree

        found: list[type] = []
        seen: set[int] = set()
        pending = [c for c, spec in components.items() if declared_here(c, spec)]
        while pending:
            component_cls = pending.pop()
            if id(component_cls) in seen or component_cls not in components:
                continue
            seen.add(id(component_cls))
            found.append(component_cls)
            spec = components[component_cls]
            pending.extend(spec.imports)
            pending.extend(spec.optional)
            for implementation in implementations.get(component_cls, []):
                pending.extend(implementation.imports)
                pending.extend(implementation.optional)
        return found

    def _parent_of(
        self,
        graph: ApplicationGraph,
        component_cls: type,
        spec: ComponentSpec,
    ) -> Optional[ContainerInjection]:
        """The container a component belongs to, declared either way round.

        `@component(module=X)` names it directly; `@module(provides=[C])` names it in
        reverse. A component named by neither is an orphan and is adopted during expansion
        by whoever first imports it.
        """
        if spec.module is not None:
            return graph.container_for(spec.module)
        for module_cls in graph.modules:
            module_spec = own_module_spec(module_cls)
            if module_spec is not None and component_cls in module_spec.provides:
                return graph.container_for(module_cls)
        return None

    def _bind_one(
        self,
        graph: ApplicationGraph,
        component_cls: type,
        spec: ComponentSpec,
        candidates: list[ImplementationSpec],
    ) -> None:
        """Bind the single implementation of one component, or fail saying why."""
        node = graph.node(component_cls)
        inline = spec.provider_factory is not None
        total = len(candidates) + (1 if inline else 0)

        if total > 1:
            named = [
                f"{c.declared_cls.__qualname__} ({c.declared_cls.__module__})"
                for c in candidates
            ]
            if inline:
                named.insert(0, f"{spec.name} itself, via provider= on @component")
            raise DeclarationError(
                f"Component {spec.name} has {total} implementations declared: "
                f"{'; '.join(named)}. Exactly one may be bound in a build. Either stop "
                f"importing the module that declares the one you do not want — that is what "
                f"an imports.py is for — or declare a second component."
            )

        imports = set(spec.imports)
        optional = set(spec.optional)
        strict = spec.strict_resolution

        if candidates:
            winner = candidates[0]
            imports |= set(winner.imports)
            optional |= set(winner.optional)
            strict = winner.strict_resolution
            implementation_cls = winner.declared_cls
            provider = winner.provider_factory(implementation_cls)
            bootstrap = winner.bootstrap
        elif inline and spec.provider_factory is not None:
            implementation_cls = component_cls
            provider = spec.provider_factory(component_cls)
            bootstrap = spec.bootstrap
        else:
            node.update_dependencies(
                imports={graph.node(i) for i in imports},
                optional={graph.node(i) for i in optional},
                strict_resolution=strict,
            )
            return

        node.set_provider(provider=provider)
        node.injectable.set_implementation(
            implementation=implementation_cls,
            modules_cls=(implementation_cls,),
            bootstrap=implementation_cls.provide if bootstrap else None,  # type: ignore[attr-defined]
        )
        node.update_dependencies(
            imports={graph.node(i) for i in imports},
            optional={graph.node(i) for i in optional},
            strict_resolution=strict,
        )
