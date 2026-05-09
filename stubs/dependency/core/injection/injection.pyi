import abc
from abc import ABC, abstractmethod
from dependency.core.exceptions import DeclarationError as DeclarationError, ProvisionError as ProvisionError
from dependency.core.injection.injectable import Injectable as Injectable
from dependency_injector import containers, providers
from typing import Any, Generator, Iterable, override

class BaseInjection(ABC, metaclass=abc.ABCMeta):
    """Base class for all nodes in the injection tree.

    Holds the node's name and its optional parent ContainerInjection.
    Subclassed by ContainerInjection (structural) and ProviderInjection (providable).
    """
    name: str
    parent: ContainerInjection | None
    def __init__(self, name: str, parent: ContainerInjection | None = None) -> None: ...
    def change_parent(self, parent: ContainerInjection | None = None) -> None:
        """Move this node to a different parent in the injection tree."""
    @abstractmethod
    def attach(self, container: containers.Container | None = None) -> None:
        """Attach this node to the dependency-injector container tree."""
    @abstractmethod
    def collect_providers(self) -> Generator['ProviderInjection', None, None]:
        """Yield all ProviderInjection nodes reachable from this node."""

class ContainerInjection(BaseInjection):
    """Structural node in the injection tree (Module, Plugin).

    Owns a DynamicContainer and organizes child nodes under a named namespace.
    The dot-separated reference path is built from the parent chain.
    """
    is_root: bool
    childs: set[BaseInjection]
    container: containers.Container
    def __init__(self, name: str, parent: ContainerInjection | None = None) -> None: ...
    @property
    def reference(self) -> str:
        """Dot-separated path used by dependency-injector for wiring."""
    @override
    def attach(self, container: containers.Container | None = None) -> None:
        """Recursively attach child nodes to this container's DynamicContainer.

        If a parent container is provided, also registers this node's
        DynamicContainer as an attribute on it, building the nested structure
        that dependency-injector uses for reference-based wiring.
        """
    @override
    def collect_providers(self) -> Generator['ProviderInjection', None, None]:
        """Yield all ProviderInjection nodes in this subtree."""

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
    is_root: bool
    imports: set['ProviderInjection']
    optional_imports: set['ProviderInjection']
    dependent: set['ProviderInjection']
    is_resolved: bool
    strict_resolution: bool
    def __init__(self, name: str, injectable: Injectable, parent: ContainerInjection | None = None, provider: providers.Provider[Any] | None = None) -> None: ...
    @property
    def reference(self) -> str:
        """Dot-separated path used by dependency-injector for wiring."""
    @property
    def injectable(self) -> Injectable:
        """The implementation binding for this provider."""
    @property
    def provider(self) -> providers.Provider[Any]:
        """The dependency-injector provider instance."""
    def set_provider(self, provider: providers.Provider[Any]) -> None:
        """Set the dependency-injector provider instance."""
    def weight(self) -> int:
        """Heuristic depth weight for graph ordering."""
    def should_resolve(self) -> bool:
        """Whether this provider can be attached to the DI container.

        Returns False if no implementation is assigned — a missing implementation
        is a declaration issue, not a resolution flag. strict_resolution controls
        error reporting during expansion, not attachment eligibility.
        """
    def resolve_if_posible(self, providers: set['ProviderInjection']) -> bool:
        """Attempt to mark this provider as resolved.

        Required imports must be resolved. Optional imports are satisfied if
        resolved OR not present in the provider set (i.e. absent by design).
        Sets is_resolved=True as a side effect and returns True if satisfied.
        """
    def update_dependencies(self, imports: Iterable['ProviderInjection'] = (), optional: Iterable['ProviderInjection'] = (), strict_resolution: bool | None = None) -> None:
        """Register required and optional imports, update resolution flags."""
    def discard_dependencies(self, imports: Iterable['ProviderInjection'] = (), optional: Iterable['ProviderInjection'] = ()) -> None:
        """Remove required and optional imports from the dependency graph."""
    @override
    def attach(self, container: containers.Container | None = None) -> None:
        """Attach this provider to the dependency-injector container."""
    @override
    def collect_providers(self) -> Generator['ProviderInjection', None, None]:
        """Yield self if eligible for resolution."""
