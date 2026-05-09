from dependency.core.injection.injection import ProviderInjection as ProviderInjection
from dependency.core.injection.mixin import ContainerMixin as ContainerMixin
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.expansion import ProviderExpansion as ProviderExpansion
from dependency.core.resolution.strategy import ResolutionStrategy as ResolutionStrategy
from typing import Iterable

class InjectionResolver:
    """Injection Resolver Class
    """
    container: Container
    def __init__(self, container: Container) -> None: ...
    def resolve_dependencies(self, modules: Iterable[type[ContainerMixin]], strategy: ResolutionStrategy = ...) -> set[ProviderInjection]: ...
    def resolve_modules(self, modules: Iterable[type[ContainerMixin]]) -> None:
        """Attach each plugin's DynamicContainer to the application container."""
    def resolve_injectables(self, modules: Iterable[type[ContainerMixin]], extra: Iterable[ProviderInjection] = ()) -> set[ProviderInjection]:
        """Build the full provider set via structural tree + import expansion.

        1. Attaches structural containers to the DI tree.
        2. Runs ProviderExpansion to collect implemented providers and discover
           undeclared ones through imports, placing orphans near their importers.
        """
    def resolve_providers(self, providers: set[ProviderInjection], strategy: ResolutionStrategy = ...) -> set[ProviderInjection]: ...
