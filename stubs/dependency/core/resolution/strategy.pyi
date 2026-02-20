from dependency.core.exceptions import CancelInitialization as CancelInitialization, DeclarationError as DeclarationError, InitializationError as InitializationError
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
    def __init__(self, config: ResolutionConfig | None = None) -> None: ...
    def resolution(self, providers: list[Injectable], container: Container) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            providers (list[Injectable]): List of providers to resolve.
            container (Container): The container to wire the injectables with.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
    def expand(self, providers: list[Injectable]) -> list[Injectable]:
        """Expand the list of providers by adding all their imports.

        Args:
            providers (list[Injectable]): List of providers to expand.

        Returns:
            list[Injectable]: List of expanded providers.
        """
    def injection(self, providers: list[Injectable]) -> None:
        """Resolve all injectables in layers.

        Args:
            providers (list[Injectable]): List of injectables to resolve.

        Returns:
            list[Injectable]: List of unresolved injectables.
        """
    def wiring(self, providers: list[Injectable], container: Container) -> None:
        """Wire a list of providers with the given container.

        Args:
            providers (list[Injectable]): List of providers to wire.
            container (Container): The container to wire the providers with.
        """
    def initialize(self, providers: list[Injectable]) -> None:
        """Start all implementations by executing their init functions.

        Args:
            providers (list[Injectable]): List of providers to start.
        """
