from dependency.core.exceptions import CancelInitialization as CancelInitialization, DeclarationError as DeclarationError, InitializationError as InitializationError
from dependency.core.injection.injection import ProviderInjection as ProviderInjection
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.errors import raise_resolution_error as raise_resolution_error
from dependency.core.resolution.expansion import ProviderExpansion as ProviderExpansion
from pydantic import BaseModel
from typing import Iterable

class ResolutionConfig(BaseModel):
    """Configuration for the Resolution Strategy."""
    init_container: bool
    legacy_resolution: bool

class ResolutionStrategy:
    """Defines the strategy for resolving dependencies."""
    config: ResolutionConfig
    def __init__(self, config: ResolutionConfig | None = None) -> None: ...
    def expand(self, providers: set[ProviderInjection]) -> set[ProviderInjection]:
        """Expand a seed set of providers by following imports transitively.

        Raises ResolutionError if any required dependency could not be resolved.
        """
    def resolution(self, providers: set[ProviderInjection], container: Container) -> list[ProviderInjection]: ...
    def injection(self, providers: set[ProviderInjection]) -> list[ProviderInjection]:
        """Resolve all providers in dependency order (layer by layer).

        Returns the order it resolved them in, which this method has always computed and
        used to throw away: every provider appears after all of its required imports, and
        providers that became resolvable together are ordered by name so two runs of the
        same graph produce the same sequence. `initialize` consumes it, which is what makes
        bootstrap order a contract instead of `set` iteration (D-053).

        Returns:
            list[ProviderInjection]: Dependency order, then name order within a layer.
        """
    def shutdown(self, providers: Iterable[ProviderInjection]) -> None:
        """Shut down every `Resource`-backed provider, in reverse of the order given.

        The mirror of `initialize`: pass the list `resolution` returned and a provider is
        torn down before the providers it imports, which is the only order in which a
        dependency is still alive while its dependents stop using it.

        This exists because the root `Container` cannot reach plugin providers — its own
        `.providers` is `['__self__']`, since plugin providers live in nested
        sub-containers attached with `setattr` — so `container.shutdown_resources()`
        silently reaches none of them (D-034). Every application had to walk the tree by
        hand; now the framework does (D-055).
        """
    def wiring(self, providers: Iterable[ProviderInjection], container: Container) -> None:
        """Wire providers against the application container."""
    def initialize(self, providers: Iterable[ProviderInjection]) -> None:
        """Execute bootstrap callables in the order given.

        Pass the list `injection` returned: a provider's required imports then bootstrap
        before it, which is what most people assume and what nothing guaranteed before
        (D-053). Passing a `set` restores the old unspecified order.
        """
