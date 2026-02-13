from typing import Iterable
from dependency.core.injection.injectable import Injectable
from dependency.core.resolution.container import Container
from dependency.core.resolution.strategy import ResolutionStrategy

class InjectionResolver:
    """Injection Resolver Class
    """
    def __init__(self,
        container: Container,
        providers: Iterable[Injectable],
    ) -> None:
        self.container: Container = container
        self.providers: list[Injectable] = list(providers)

    def resolve_dependencies(self,
        strategy: type[ResolutionStrategy] = ResolutionStrategy
    ) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            strategy (type[ResolutionStrategy]): The resolution strategy to use.

        Returns:
            list[Injectable]: List of resolved injectables."""
        return strategy.resolution(
            container=self.container,
            providers=self.providers,
        )
