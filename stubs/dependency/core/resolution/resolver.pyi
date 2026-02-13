from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.resoluble import ResolubleProvider as ResolubleProvider
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.strategy import ResolutionStrategy as ResolutionStrategy
from typing import Iterable

class InjectionResolver:
    """Injection Resolver Class
    """
    container: Container
    providers: list[ResolubleProvider]
    def __init__(self, container: Container, providers: Iterable[ResolubleProvider]) -> None: ...
    def resolve_dependencies(self, strategy: type[ResolutionStrategy] = ...) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            strategy (type[ResolutionStrategy]): The resolution strategy to use.

        Returns:
            list[Injectable]: List of resolved injectables."""
