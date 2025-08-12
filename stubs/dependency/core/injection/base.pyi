import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from dependency_injector import containers
from typing import Any, Callable, Generator

class BaseInjection(ABC, metaclass=abc.ABCMeta):
    def __init__(self, name: str, parent: ContainerInjection | None = None) -> None: ...
    @property
    def name(self) -> str:
        """Return the name of the injection."""
    @property
    def reference(self) -> str:
        """Return the reference for dependency injection."""
    @abstractmethod
    def inject_cls(self) -> Any:
        """Return the class to be injected."""
    @abstractmethod
    def resolve_providers(self) -> Generator['ProviderInjection', None, None]:
        """Inject all children into the current injection context."""

class ContainerInjection(BaseInjection):
    childs: list[BaseInjection]
    container: Incomplete
    def __init__(self, name: str, parent: ContainerInjection | None = None) -> None: ...
    def inject_cls(self) -> containers.DynamicContainer:
        """Return the container instance."""
    def resolve_providers(self) -> Generator['ProviderInjection', None, None]:
        """Inject all children into the current injection context."""

class ProviderDependency:
    name: str
    provided_cls: type
    imports: list['ProviderInjection']
    def __init__(self, name: str, provided_cls: type, imports: list['ProviderInjection']) -> None: ...

class ProviderInjection(BaseInjection):
    component_name: str
    interface_cls: type
    provider_cls: type
    modules_cls: set[type]
    imports: list['ProviderInjection']
    depends: list[ProviderDependency]
    bootstrap: Callable | None
    def __init__(self, name: str, component_name: str, interface_cls: type, parent: ContainerInjection | None = None) -> None: ...
    @property
    def provided_cls(self) -> type:
        """Return the provided class."""
    def inject_cls(self) -> Any:
        """Return the provider instance."""
    def resolve_providers(self) -> Generator['ProviderInjection', None, None]:
        """Inject all children into the current injection context."""
    def set_implementation(self, provided_cls: type, provider_cls: type, component_cls: type, imports: list['ProviderInjection'] = [], depends: list[ProviderDependency] = [], bootstrap: Callable | None = None) -> None:
        '''Set the parameters for the provider.

        Args:
            provided_cls (type): The class that is provided by the provider.
            provider_cls (type): The class that is used to create the provider.
            component_cls (type): The class of the component that is being provided.
            imports (list["ProviderInjection"], optional): A list of provider injections that are imported by this provider.
            depends (list[ProviderDependency], optional): A list of provider dependencies for this provider.
            bootstrap (Optional[Callable], optional): A bootstrap function for the provider.
        '''
    @property
    def dependency(self) -> ProviderDependency:
        """Return the dependency information for the provider."""
    def add_wire_cls(self, wire_cls: type) -> None:
        """Add a class to the set of modules that need to be wired."""
    def do_prewiring(self) -> None:
        """Declare all modules that need to be wired on their respective providers."""
    def do_bootstrap(self, container: containers.DynamicContainer) -> None:
        """Wire all modules with their dependencies and bootstrap required components.

        Args:
            container (containers.DynamicContainer): The container to bootstrap the provider in.
        """
