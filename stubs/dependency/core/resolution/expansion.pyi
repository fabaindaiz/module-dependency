from dataclasses import dataclass, field
from dependency.core.exceptions import ResolutionError as ResolutionError
from dependency.core.injection.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection
from dependency.core.injection.mixin import ContainerMixin as ContainerMixin
from typing import Iterable

@dataclass
class ResolutionNode:
    """A provider being tracked through the expansion BFS.

    Attributes:
        provider: The injection node being processed.
        context: The nearest parent ContainerInjection (from the importer).
        imported_by: Backpointer to the node that first imported this one.
    """
    provider: ProviderInjection
    context: ContainerInjection | None
    imported_by: ResolutionNode | None = field(default=None, repr=False)
    def import_chain(self) -> list[ProviderInjection]:
        """Return the import path from the root seed down to this node."""

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
    def __init__(self, modules: Iterable[type[ContainerMixin]], extra: Iterable[ProviderInjection] = ()) -> None: ...
    def expand(self) -> ExpansionResult:
        """Run the full expansion and return resolved + failed providers."""
