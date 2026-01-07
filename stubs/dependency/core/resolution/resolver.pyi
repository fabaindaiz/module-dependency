from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.errors import raise_resolution_error as raise_resolution_error
from pydantic import BaseModel
from typing import Iterable

class InjectionConfig(BaseModel):
    """Configuration for the Injection Resolver.
    """
    resolve_products: bool

class InjectionResolver:
    """Injection Resolver Class
    """
    container: Container
    def __init__(self, container: Container, injectables: Iterable[Injectable]) -> None: ...
    def resolve_dependencies(self, config: InjectionConfig = ...) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            config (InjectionConfig): Configuration for the injection resolver.

        Returns:
            list[Injectable]: List of resolved injectables."""
    @classmethod
    def resolution(cls, container: Container, injectables: list[Injectable], config: InjectionConfig = ...) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            container (Container): The container to wire the injectables with.
            injectables (list[Injectable]): List of injectables to resolve.
            config (InjectionConfig): Configuration for the injection resolver.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
    @staticmethod
    def injection(injectables: list[Injectable], config: InjectionConfig = ...) -> list[Injectable]:
        """Resolve all injectables in layers.

        Args:
            container (Container): The container to wire the injectables with.
            injectables (list[Injectable]): List of injectables to resolve.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
    @staticmethod
    def wiring(container: Container, injectables: list[Injectable]) -> None:
        """Wire a list of injectables with the given container.

        Args:
            container (Container): The container to wire the injectables with.
            injectables (list[Injectable]): List of injectables to wire.
        """
    @staticmethod
    def bootstrap(injectables: list[Injectable]) -> None:
        """Start all implementations by executing their bootstrap functions.

        Args:
            injectables (list[Injectable]): List of injectables to start.
        """
