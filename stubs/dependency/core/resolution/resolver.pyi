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
    def __init__(self, container: Container) -> None: ...
    def resolve_dependencies(self, modules: Iterable[type[ContainerMixin]], strategy: ResolutionStrategy = ...) -> list[Injectable]:
        """Resolve dependencies for a list of modules.

        Args:
            modules (Iterable[type[ContainerMixin]]): The list of module classes to resolve.
            strategy (type[ResolutionStrategy]): The resolution strategy to use.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
    def resolve_modules(self, modules: Iterable[type[ContainerMixin]]) -> list[Injectable]:
        """Resolve all modules and their dependencies.

        Args:
            modules (Iterable[type[ContainerMixin]]): The list of module classes to resolve.

        Returns:
            list[Injectable]: List of resolved injectables from the modules.
        """
    def resolve_providers(self, providers: Iterable[Injectable], strategy: ResolutionStrategy = ...) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            providers (Iterable[Injectable]): The list of providers to resolve.
            strategy (type[ResolutionStrategy]): The resolution strategy to use.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
