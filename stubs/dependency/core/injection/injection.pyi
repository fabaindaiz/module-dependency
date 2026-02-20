import abc
from abc import ABC, abstractmethod
from dependency.core.exceptions import DeclarationError as DeclarationError, ProvisionError as ProvisionError
from dependency.core.injection.injectable import Injectable as Injectable
from dependency_injector import containers, providers as providers
from typing import Any, Generator, override

class BaseInjection(ABC, metaclass=abc.ABCMeta):
    """Base Injection Class
    """
    is_root: bool
    name: str
    parent: ContainerInjection | None
    def __init__(self, name: str, parent: ContainerInjection | None = None) -> None: ...
    @property
    def reference(self) -> str:
        """Return the reference for dependency injection."""
    def change_parent(self, parent: ContainerInjection | None = None) -> None:
        """Change the parent injection of this injection.

        Args:
            parent (ContainerInjection): The new parent injection.
        """
    @abstractmethod
    def inject_cls(self) -> Any:
        """Return the class to be injected."""
    @abstractmethod
    def resolve_providers(self) -> Generator[Injectable, None, None]:
        """Inject all children into the current injection context."""

class ContainerInjection(BaseInjection):
    """Container Injection Class
    """
    childs: set[BaseInjection]
    container: containers.Container
    def __init__(self, name: str, parent: ContainerInjection | None = None) -> None: ...
    @override
    def inject_cls(self) -> containers.Container:
        """Return the container instance."""
    @override
    def resolve_providers(self) -> Generator[Injectable, None, None]:
        """Inject all children into the current container."""

class ProviderInjection(BaseInjection):
    """Provider Injection Class
    """
    def __init__(self, name: str, injectable: Injectable, parent: ContainerInjection | None = None, provider: providers.Provider[Any] | None = None) -> None: ...
    def set_provider(self, provider: providers.Provider[Any]) -> None:
        """Set the provider instance for this injectable.

        Args:
            provider (providers.Provider[Any]): The provider instance to set.
        """
    @property
    def injectable(self) -> Injectable:
        """Return the injectable instance for this provider."""
    @property
    @override
    def reference(self) -> str:
        """Return the reference for dependency injection."""
    @property
    def provider(self) -> providers.Provider[Any]:
        """Return the provider instance for this injectable."""
    @override
    def inject_cls(self) -> providers.Provider[Any]:
        """Return the provider instance."""
    @override
    def resolve_providers(self) -> Generator[Injectable, None, None]:
        """Inject all imports into the current injectable."""
