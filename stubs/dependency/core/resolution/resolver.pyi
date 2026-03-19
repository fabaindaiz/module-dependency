from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.mixin import ContainerMixin as ContainerMixin
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.registry import Registry as Registry
from dependency.core.resolution.strategy import ResolutionStrategy as ResolutionStrategy
from typing import Iterable

class InjectionResolver:
    """Injection Resolver Class
    """
    container: Container
    def __init__(self, container: Container) -> None:
        """Initialize the resolver with the application container.

        Args:
            container (Container): The root application container that providers
                will be injected into and wired against.
        """
    def resolve_dependencies(self, modules: Iterable[type[ContainerMixin]], strategy: ResolutionStrategy = ...) -> set[Injectable]:
        """Resolve dependencies for a list of modules.

        Args:
            modules (Iterable[type[ContainerMixin]]): The list of module classes to resolve.
            strategy (type[ResolutionStrategy]): The resolution strategy to use.

        Returns:
            set[Injectable]: List of resolved injectables.
        """
    def resolve_modules(self, modules: Iterable[type[ContainerMixin]]) -> None:
        """Resolve all modules and initialize them.

        Args:
            modules (Iterable[type[ContainerMixin]]): The set of module classes to resolve.
        """
    def resolve_injectables(self, modules: Iterable[type[ContainerMixin]]) -> set[Injectable]:
        """Resolve all injectables from a set of modules.

        Args:
            modules (Iterable[type[ContainerMixin]]): The set of module classes to resolve.
        Returns:
            set[Injectable]: Set of resolved injectables.
        """
    def resolve_providers(self, providers: set[Injectable], strategy: ResolutionStrategy = ...) -> set[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            providers (Iterable[Injectable]): The set of providers to resolve.
            strategy (type[ResolutionStrategy]): The resolution strategy to use.

        Returns:
            set[Injectable]: Set of resolved injectables.
        """
