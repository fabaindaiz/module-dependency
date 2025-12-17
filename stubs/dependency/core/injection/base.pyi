import abc
from abc import ABC, abstractmethod
from dependency.core.injection.injectable import Injectable as Injectable
from dependency_injector import containers
from typing import Any, Generator

class ABCInjection(ABC):
    """Injectable Holder Interface
    """
    injectable: BaseInjection
    def change_parent(self, parent: ContainerInjection) -> None:
        """Change the parent injection of this injection.

        Args:
            parent (ContainerInjection): The new parent injection.
        """

class BaseInjection(ABC, metaclass=abc.ABCMeta):
    """Base Injection Class
    """
    name: str
    parent: ContainerInjection | None
    def __init__(self, name: str, parent: ContainerInjection | None = None) -> None: ...
    @property
    def reference(self) -> str:
        """Return the reference for dependency injection."""
    @abstractmethod
    def inject_cls(self) -> Any:
        """Return the class to be injected."""
    @abstractmethod
    def resolve_providers(self) -> Generator[Injectable, None, None]:
        """Inject all children into the current injection context."""

class ContainerInjection(BaseInjection):
    """Container Injection Class
    """
    childs: list[BaseInjection]
    container: containers.Container
    def __init__(self, name: str, parent: ContainerInjection | None = None) -> None: ...
    def inject_cls(self) -> containers.Container:
        """Return the container instance."""
    def resolve_providers(self) -> Generator[Injectable, None, None]:
        """Inject all children into the current container."""
