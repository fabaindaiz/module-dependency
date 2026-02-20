import logging
from abc import ABC, abstractmethod
from typing import Any, Generator, Optional, override
from dependency_injector import containers, providers
from dependency.core.injection.injectable import Injectable
from dependency.core.exceptions import DeclarationError, ProvisionError
_logger = logging.getLogger("dependency.loader")

class BaseInjection(ABC):
    """Base Injection Class
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
    def inject_cls(self) -> Any:
        """Return the class to be injected."""

    @abstractmethod
    def resolve_providers(self) -> Generator[Injectable, None, None]:
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
    def inject_cls(self) -> containers.Container:
        """Return the container instance."""
        return self.container

    @override
    def resolve_providers(self) -> Generator[Injectable, None, None]:
        """Inject all children into the current container."""
        for child in self.childs:
            setattr(self.container, child.name, child.inject_cls())
            yield from child.resolve_providers()

class ProviderInjection(BaseInjection):
    """Provider Injection Class
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
    def inject_cls(self) -> providers.Provider[Any]:
        """Return the provider instance."""
        return self.provider

    @override
    def resolve_providers(self) -> Generator[Injectable, None, None]:
        """Inject all imports into the current injectable."""
        yield self._injectable
