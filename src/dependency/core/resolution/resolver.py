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
        """Initialize the resolver with the application container.

        Args:
            container (Container): The root application container that providers
                will be injected into and wired against.
        """
        self.container: Container = container

    def resolve_dependencies(self,
        modules: Iterable[type[ContainerMixin]],
        strategy: ResolutionStrategy = ResolutionStrategy()
    ) -> set[Injectable]:
        """Resolve dependencies for a list of modules.

        Args:
            modules (Iterable[type[ContainerMixin]]): The list of module classes to resolve.
            strategy (type[ResolutionStrategy]): The resolution strategy to use.

        Returns:
            set[Injectable]: List of resolved injectables.
        """
        self.resolve_modules(
            modules=modules
        )
        providers = self.resolve_injectables(
            modules=modules,
        )
        return self.resolve_providers(
            providers=providers,
            strategy=strategy
        )

    def resolve_modules(self,
        modules: Iterable[type[ContainerMixin]],
    ) -> None:
        """Resolve all modules and initialize them.

        Args:
            modules (Iterable[type[ContainerMixin]]): The set of module classes to resolve.
        """

        for module in modules:
            module.inject_container(container=self.container)

    def resolve_injectables(self,
        modules: Iterable[type[ContainerMixin]],
    ) -> set[Injectable]:
        """Resolve all injectables from a set of modules.

        Args:
            modules (Iterable[type[ContainerMixin]]): The set of module classes to resolve.
        Returns:
            set[Injectable]: Set of resolved injectables.
        """
        injectables: set[Injectable] = set()
        for module in modules:
            module.resolve_providers()
            injectables.update(module.resolve_injectables())
        return injectables

    def resolve_providers(self,
        providers: set[Injectable],
        strategy: ResolutionStrategy = ResolutionStrategy()
    ) -> set[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            providers (Iterable[Injectable]): The set of providers to resolve.
            strategy (type[ResolutionStrategy]): The resolution strategy to use.

        Returns:
            set[Injectable]: Set of resolved injectables.
        """
        Registry.validation()
        return strategy.resolution(
            container=self.container,
            providers=providers,
        )
