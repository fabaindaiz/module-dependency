from dependency.core.exceptions import CancelInitialization as CancelInitialization, DeclarationError as DeclarationError, InitializationError as InitializationError
from dependency.core.injection.injection import ProviderInjection as ProviderInjection
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.errors import raise_resolution_error as raise_resolution_error
from dependency.core.resolution.expansion import ProviderExpansion as ProviderExpansion
from pydantic import BaseModel
from typing import Iterable

class ResolutionConfig(BaseModel):
    """Configuration for the Resolution Strategy.
    """
    init_container: bool
    legacy_resolution: bool

class ResolutionStrategy:
    """Defines the strategy for resolving dependencies.
    """
    config: ResolutionConfig
    def __init__(self, config: ResolutionConfig | None = None) -> None: ...
    def expand(self, providers: set[ProviderInjection]) -> set[ProviderInjection]:
        """Expand a seed set of providers by following imports transitively.

        Raises ResolutionError if any required dependency could not be resolved.
        """
    def resolution(self, providers: set[ProviderInjection], container: Container) -> set[ProviderInjection]: ...
    def injection(self, providers: set[ProviderInjection]) -> None:
        """Resolve all providers in dependency order (layer by layer)."""
    def wiring(self, providers: Iterable[ProviderInjection], container: Container) -> None:
        """Wire providers against the application container."""
    def initialize(self, providers: Iterable[ProviderInjection]) -> None:
        """Execute bootstrap callables for eagerly-instantiated providers."""
