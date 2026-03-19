import logging
from abc import ABC, abstractmethod
from typing import Any, Generator, Optional, override
from dependency_injector import containers, providers
from dependency.core.injection.injectable import Injectable
from dependency.core.exceptions import DeclarationError, ProvisionError
_logger = logging.getLogger("dependency.loader")

class BaseInjection(ABC):
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
    def __init__(self,
        name: str,
        parent: Optional['ContainerInjection'] = None
    ) -> None:
        self.is_root: bool = False
        self.name: str = name
        self.parent: Optional['ContainerInjection'] = parent
        if self.parent:
            self.parent.childs.add(self)

    @property
    def reference(self) -> str:
        """Return the reference for dependency injection."""
        if not self.parent:
            return self.name
        return f"{self.parent.reference}.{self.name}"

    def change_parent(self, parent: Optional['ContainerInjection'] = None) -> None:
        """Change the parent injection of this injection.

        Args:
            parent (ContainerInjection): The new parent injection.
        """
        if self.parent is not None:
            self.parent.childs.remove(self)
        self.parent = parent
        if self.parent is not None:
            self.parent.childs.add(self)

    @abstractmethod
    def resolve_providers(self, container: Optional[containers.Container] = None) -> None:
        """Resolve the injection context."""

    @abstractmethod
    def resolve_injectables(self) -> Generator[Injectable, None, None]:
        """Inject all children into the current injection context."""

    def __repr__(self) -> str:
        return self.name

class ContainerInjection(BaseInjection):
    """Container Injection Class
    """
    def __init__(self,
        name: str,
        parent: Optional['ContainerInjection'] = None
    ) -> None:
        super().__init__(name=name, parent=parent)
        self.childs: set[BaseInjection] = set()
        self.container: containers.Container = containers.DynamicContainer()

    @override
    def resolve_providers(self,container: Optional[containers.Container] = None) -> None:
        """Recursively attach all child providers to this container's DynamicContainer.

        If a parent container is provided, also registers this node's DynamicContainer
        as an attribute on it, building the nested container structure that
        dependency-injector uses for reference-based wiring.

        Args:
            container (containers.Container, optional): The parent container to attach
                this node's DynamicContainer to, if any.
        """
        if container is not None:
            setattr(container, self.name, self.container)
        for child in self.childs:
            child.resolve_providers(container=self.container)

    @override
    def resolve_injectables(self) -> Generator[Injectable, None, None]:
        """Inject all children into the current container."""
        for child in self.childs:
            yield from child.resolve_injectables()

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
    def __init__(self,
        name: str,
        injectable: Injectable,
        parent: Optional['ContainerInjection'] = None,
        provider: Optional[providers.Provider[Any]] = None,
    ) -> None:
        super().__init__(name=name, parent=parent)
        self._injectable: Injectable = injectable
        self._provider: Optional[providers.Provider[Any]] = provider

    def set_provider(self, provider: providers.Provider[Any]) -> None:
        """Set the provider instance for this injectable.

        Args:
            provider (providers.Provider[Any]): The provider instance to set.
        """
        self._provider = provider

    @property
    def injectable(self) -> Injectable:
        """Return the injectable instance for this provider."""
        return self._injectable

    @property
    @override
    def reference(self) -> str:
        """Return the reference for dependency injection."""
        if not self.parent:
            raise ProvisionError(f"Provider {self.name} requires a parent container for reference-based injection")
        return f"{self.parent.reference}.{self.name}"

    @property
    def provider(self) -> providers.Provider[Any]:
        """Return the provider instance for this injectable."""
        if self._provider is None:
            raise DeclarationError(f"Provider {self} has no implementation assigned")
        return self._provider

    @override
    def resolve_providers(self, container: Optional[containers.Container] = None) -> None:
        """Return the provider instance."""
        if container is not None and self._injectable.has_implementation():
            setattr(container, self.name, self.provider)

    @override
    def resolve_injectables(self) -> Generator[Injectable, None, None]:
        """Inject all imports into the current injectable."""
        if self._injectable.has_implementation():
            yield self._injectable
