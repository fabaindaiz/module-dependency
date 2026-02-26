from typing import Iterable
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.mixin import ContainerMixin
from dependency.core.resolution.container import Container
from dependency.core.resolution.registry import Registry
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
    ) -> list[Injectable]:
        """Resolve dependencies for a list of modules.

        Args:
            modules (Iterable[type[ContainerMixin]]): The list of module classes to resolve.
            strategy (type[ResolutionStrategy]): The resolution strategy to use.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
        Registry.validation()
        providers = self.resolve_modules(
            modules=modules
        )
        return self.resolve_providers(
            providers=providers,
            strategy=strategy
        )

    def resolve_modules(self,
        modules: Iterable[type[ContainerMixin]],
    ) -> list[Injectable]:
        """Resolve all modules and their dependencies.

        Args:
            modules (Iterable[type[ContainerMixin]]): The list of module classes to resolve.

        Returns:
            list[Injectable]: List of resolved injectables from the modules.
        """
        providers: list[Injectable] = []

        for module in modules:
            providers.extend(module.resolve_injectables())
            module.inject_container(container=self.container)

        return providers

    def resolve_providers(self,
        providers: Iterable[Injectable],
        strategy: ResolutionStrategy = ResolutionStrategy()
    ) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            providers (Iterable[Injectable]): The list of providers to resolve.
            strategy (type[ResolutionStrategy]): The resolution strategy to use.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
        return strategy.resolution(
            container=self.container,
            providers=list(providers),
        )
