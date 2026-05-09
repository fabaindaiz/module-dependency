import logging
from abc import ABC, abstractmethod
from typing import Any, Generator, Iterable, Optional, override
from dependency_injector import containers, providers
from dependency.core.injection.injectable import Injectable
from dependency.core.exceptions import DeclarationError, ProvisionError
_logger = logging.getLogger("dependency.loader")

class BaseInjection(ABC):
    """Base class for all nodes in the injection tree.

    Holds the node's name and its optional parent ContainerInjection.
    Subclassed by ContainerInjection (structural) and ProviderInjection (providable).
    """
    def __init__(self,
        name: str,
        parent: Optional['ContainerInjection'] = None,
    ) -> None:
        self.name: str = name
        self.parent: Optional['ContainerInjection'] = parent
        if self.parent:
            self.parent.childs.add(self)

    def change_parent(self, parent: Optional['ContainerInjection'] = None) -> None:
        """Move this node to a different parent in the injection tree."""
        if self.parent is not None:
            self.parent.childs.remove(self)
        self.parent = parent
        if self.parent is not None:
            self.parent.childs.add(self)

    @abstractmethod
    def attach(self, container: Optional[containers.Container] = None) -> None:
        """Attach this node to the dependency-injector container tree."""

    @abstractmethod
    def collect_providers(self) -> Generator['ProviderInjection', None, None]:
        """Yield all ProviderInjection nodes reachable from this node."""

    def __repr__(self) -> str:
        return self.name


class ContainerInjection(BaseInjection):
    """Structural node in the injection tree (Module, Plugin).

    Owns a DynamicContainer and organizes child nodes under a named namespace.
    The dot-separated reference path is built from the parent chain.
    """
    def __init__(self,
        name: str,
        parent: Optional['ContainerInjection'] = None,
    ) -> None:
        super().__init__(name=name, parent=parent)
        self.is_root: bool = False
        self.childs: set[BaseInjection] = set()
        self.container: containers.Container = containers.DynamicContainer()

    @property
    def reference(self) -> str:
        """Dot-separated path used by dependency-injector for wiring."""
        if not self.parent:
            return self.name
        return f"{self.parent.reference}.{self.name}"

    @override
    def attach(self, container: Optional[containers.Container] = None) -> None:
        """Recursively attach child nodes to this container's DynamicContainer.

        If a parent container is provided, also registers this node's
        DynamicContainer as an attribute on it, building the nested structure
        that dependency-injector uses for reference-based wiring.
        """
        if container is not None:
            setattr(container, self.name, self.container)
        for child in self.childs:
            child.attach(container=self.container)

    @override
    def collect_providers(self) -> Generator['ProviderInjection', None, None]:
        """Yield all ProviderInjection nodes in this subtree."""
        for child in self.childs:
            yield from child.collect_providers()


class ProviderInjection(BaseInjection):
    """Providable leaf node in the injection tree (Component, Product).

    Owns the dependency graph tracking and resolution state. The Injectable
    holds only the implementation binding (interface -> concrete class).

    Attributes:
        imports: ProviderInjection nodes this provider depends on.
        dependent: ProviderInjection nodes that depend on this provider.
        is_resolved: Whether this provider has been fully resolved.
        partial_resolution: If True, imports outside the current set are not required.
        strict_resolution: If False, resolution proceeds even without implementation.
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
        self.is_root: bool = False

        self.imports: set['ProviderInjection'] = set()
        self.optional_imports: set['ProviderInjection'] = set()
        self.dependent: set['ProviderInjection'] = set()
        self._weight: Optional[int] = None

        self.is_resolved: bool = False
        self.strict_resolution: bool = True

    @property
    def reference(self) -> str:
        """Dot-separated path used by dependency-injector for wiring."""
        if not self.parent:
            raise ProvisionError(f"Provider {self.name} requires a parent container for reference-based injection")
        return f"{self.parent.reference}.{self.name}"

    @property
    def injectable(self) -> Injectable:
        """The implementation binding for this provider."""
        return self._injectable

    @property
    def provider(self) -> providers.Provider[Any]:
        """The dependency-injector provider instance."""
        if self._provider is None:
            raise DeclarationError(f"Provider {self} has no implementation assigned")
        return self._provider

    def set_provider(self, provider: providers.Provider[Any]) -> None:
        """Set the dependency-injector provider instance."""
        self._provider = provider

    def weight(self) -> int:
        """Heuristic depth weight for graph ordering."""
        if self._weight is None:
            all_imports = self.imports | self.optional_imports
            self._weight = len(all_imports) + sum(d.weight() for d in all_imports)
        return self._weight

    def should_resolve(self) -> bool:
        """Whether this provider can be attached to the DI container.

        Returns False if no implementation is assigned — a missing implementation
        is a declaration issue, not a resolution flag. strict_resolution controls
        error reporting during expansion, not attachment eligibility.
        """
        if self._injectable.implementation is None:
            if not self.strict_resolution:
                _logger.warning(f"Provider {self.name} has no implementation assigned")
            return False
        return True

    def resolve_if_posible(self, providers: set['ProviderInjection']) -> bool:
        """Attempt to mark this provider as resolved.

        Required imports must be resolved. Optional imports are satisfied if
        resolved OR not present in the provider set (i.e. absent by design).
        Sets is_resolved=True as a side effect and returns True if satisfied.
        """
        if self._injectable.implementation is None:
            return False

        for imported in self.imports:
            if not imported.is_resolved:
                return False

        for imported in self.optional_imports:
            if not (imported.is_resolved or imported not in providers):
                return False

        self.is_resolved = True
        return True

    def update_dependencies(self,
        imports: Iterable['ProviderInjection'] = (),
        optional: Iterable['ProviderInjection'] = (),
        strict_resolution: Optional[bool] = None,
    ) -> None:
        """Register required and optional imports, update resolution flags."""
        self.imports.update(imports)
        for i in imports:
            i.dependent.add(self)
        self.optional_imports.update(optional)
        for i in optional:
            i.dependent.add(self)
        if strict_resolution is not None:
            self.strict_resolution = strict_resolution

    def discard_dependencies(self,
        imports: Iterable['ProviderInjection'] = (),
        optional: Iterable['ProviderInjection'] = (),
    ) -> None:
        """Remove required and optional imports from the dependency graph."""
        self.imports.difference_update(imports)
        for i in imports:
            i.dependent.discard(self)
        self.optional_imports.difference_update(optional)
        for i in optional:
            i.dependent.discard(self)

    @override
    def attach(self, container: Optional[containers.Container] = None) -> None:
        """Attach this provider to the dependency-injector container."""
        if container is not None and self.should_resolve():
            setattr(container, self.name, self.provider)

    @override
    def collect_providers(self) -> Generator['ProviderInjection', None, None]:
        """Yield self if eligible for resolution."""
        if self.should_resolve():
            yield self
