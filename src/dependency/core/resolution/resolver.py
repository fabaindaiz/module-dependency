from typing import Iterable
from dependency.core.injection.injection import ProviderInjection
from dependency.core.injection.mixin import ContainerMixin
from dependency.core.resolution.container import Container
from dependency.core.resolution.expansion import ProviderExpansion
from dependency.core.resolution.strategy import ResolutionStrategy

class InjectionResolver:
    """Injection Resolver Class
    """
    def __init__(self,
        container: Container,
    ) -> None:
        self.container: Container = container

    def resolve_dependencies(self,
        modules: Iterable[type[ContainerMixin]],
        strategy: ResolutionStrategy = ResolutionStrategy()
    ) -> set[ProviderInjection]:
        self.resolve_modules(modules=modules)
        providers = self.resolve_injectables(modules=modules)
        return self.resolve_providers(providers=providers, strategy=strategy)

    def resolve_modules(self,
        modules: Iterable[type[ContainerMixin]],
    ) -> None:
        """Attach each plugin's DynamicContainer to the application container."""
        for module in modules:
            module.inject_container(container=self.container)

    def resolve_injectables(self,
        modules: Iterable[type[ContainerMixin]],
        extra: Iterable[ProviderInjection] = (),
    ) -> set[ProviderInjection]:
        """Build the full provider set via structural tree + import expansion.

        1. Attaches structural containers to the DI tree.
        2. Runs ProviderExpansion to collect implemented providers and discover
           undeclared ones through imports, placing orphans near their importers.
        """
        modules = list(modules)
        for module in modules:
            module.resolve_providers()

        result = ProviderExpansion(modules=modules, extra=extra).expand()
        result.raise_if_failed()
        return result.resolved

    def resolve_providers(self,
        providers: set[ProviderInjection],
        strategy: ResolutionStrategy = ResolutionStrategy()
    ) -> set[ProviderInjection]:
        return strategy.resolution(
            container=self.container,
            providers=providers,
        )
