import abc
from abc import ABC, abstractmethod
from dependency.core.exceptions import DeclarationError as DeclarationError, ProvisionError as ProvisionError
from dependency.core.injection.injectable import Injectable as Injectable
from dependency_injector import containers, providers as providers
from typing import Any, Generator, override

class BaseInjection(ABC, metaclass=abc.ABCMeta):
    """Base class for all nodes in the injection tree.

    Holds the node's name, its optional parent ContainerInjection, and the
    dot-separated reference path used by dependency-injector for wiring.
    Subclassed by ContainerInjection (for structural units) and
    ProviderInjection (for providable units).

    Attributes:
        is_root (bool): True if this node is a root (Plugin), meaning it has
            no parent by design and should not be treated as orphan.
        name (str): The class name of the decorated unit.
        parent (ContainerInjection, optional): The parent node in the tree.
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
    def resolve_providers(self, container: containers.Container | None = None) -> None:
        """Resolve the injection context."""
    @abstractmethod
    def resolve_injectables(self) -> Generator[Injectable, None, None]:
        """Inject all children into the current injection context."""

class ContainerInjection(BaseInjection):
    """Container Injection Class
    """
    childs: set[BaseInjection]
    container: containers.Container
    def __init__(self, name: str, parent: ContainerInjection | None = None) -> None: ...
    @override
    def resolve_providers(self, container: containers.Container | None = None) -> None:
        """Recursively attach all child providers to this container's DynamicContainer.

        If a parent container is provided, also registers this node's DynamicContainer
        as an attribute on it, building the nested container structure that
        dependency-injector uses for reference-based wiring.

        Args:
            container (containers.Container, optional): The parent container to attach
                this node's DynamicContainer to, if any.
        """
    @override
    def resolve_injectables(self) -> Generator[Injectable, None, None]:
        """Inject all children into the current container."""

class ProviderInjection(BaseInjection):
    """Injection node for a providable unit (Component or Product).

    Holds the ProviderInjection's Injectable and the underlying
    dependency-injector Provider instance. Participates in the injection
    tree as a leaf node — it has a parent ContainerInjection but no children.

    Attributes:
        _injectable (Injectable): Tracks the implementation, imports, and
            resolution state for this provider.
        _provider (providers.Provider, optional): The dependency-injector
            provider instance (Singleton, Factory, or Resource).
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
    def resolve_providers(self, container: containers.Container | None = None) -> None:
        """Return the provider instance."""
    @override
    def resolve_injectables(self) -> Generator[Injectable, None, None]:
        """Inject all imports into the current injectable."""
