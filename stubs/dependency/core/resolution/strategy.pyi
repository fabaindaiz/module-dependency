from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.errors import raise_resolution_error as raise_resolution_error
from pydantic import BaseModel

class ResolutionConfig(BaseModel):
    """Configuration for the Resolution Strategy.
    """
    init_container: bool

class ResolutionStrategy:
    """Defines the strategy for resolving dependencies.
    """
    config: ResolutionConfig
    @classmethod
    def resolution(cls, providers: list[Injectable], container: Container) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            providers (list[Injectable]): List of providers to resolve.
            container (Container): The container to wire the injectables with.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
    @classmethod
    def expand(cls, providers: list[Injectable]) -> list[Injectable]:
        """Expand the list of providers by adding their imports.

        Args:
            providers (list[Injectable]): List of injectables to search.
        """
    @classmethod
    def injection(cls, providers: list[Injectable]) -> list[Injectable]:
        """Resolve all injectables in layers.

        Args:
            providers (list[Injectable]): List of injectables to resolve.

        Returns:
            list[Injectable]: List of unresolved injectables.
        """
    @classmethod
    def validation(cls, providers: list[Injectable], unresolved: list[Injectable]) -> None:
        """Validate that all unresolved injectables are in the list of providers.

        Args:
            providers (list[Injectable]): List of providers to validate.
            unresolved (list[Injectable]): List of unresolved injectables.
        """
    @classmethod
    def wiring(cls, providers: list[Injectable], container: Container) -> None:
        """Wire a list of providers with the given container.

        Args:
            providers (list[Injectable]): List of providers to wire.
            container (Container): The container to wire the providers with.
        """
    @classmethod
    def initialize(cls, providers: list[Injectable]) -> None:
        """Start all implementations by executing their init functions.

        Args:
            providers (list[Injectable]): List of providers to start.
        """
