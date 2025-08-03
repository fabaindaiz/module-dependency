from abc import ABC, abstractmethod
from dependency_injector import containers
from typing import Any, Generator, Optional
from dependency.core.declaration.base import ABCComponent
from dependency.core.exceptions import DependencyError

class BaseInjection(ABC):
    def __init__(self, name: str) -> None:
        self.parent: Optional["BaseInjection"] = None
        self.name: str = name
    
    @property
    def reference(self) -> str:
        if self.parent:
            return f"{self.parent.reference}.{self.name}"
        return self.name
    
    @abstractmethod
    def inject_cls(self) -> Any:
        """Return the class to be injected."""
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    @abstractmethod
    def child_add(self, child: "BaseInjection") -> None:
        """Add a child injection to the current injection context."""
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    @abstractmethod
    def child_inject(self) -> Generator['ProviderInjection', None, None]:
        """Inject all children into the current injection context."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abstractmethod
    def child_wire(self, container: containers.DynamicContainer) -> None:
        """Wire the injection into the provided container."""
        raise NotImplementedError("This method should be implemented by subclasses.")

class ContainerInjection(BaseInjection):
    def __init__(self,
            name: str
            ) -> None:
        self.__childs: list[BaseInjection] = []
        self.container = containers.DynamicContainer()
        super().__init__(name)
    
    def inject_cls(self) -> containers.DynamicContainer:
        """Return the container instance."""
        return self.container

    def child_add(self, child: BaseInjection) -> None:
        self.__childs.append(child)
        child.parent = self
    
    def child_inject(self) -> Generator['ProviderInjection', None, None]:
        for child in self.__childs:
            setattr(self.container, child.name, child.inject_cls())
            yield from child.child_inject()

    def child_wire(self, container: containers.DynamicContainer) -> None:
        """Wire all child injections into the provided container."""
        for child in self.__childs:
            child.child_wire(container)

class ProviderInjection(BaseInjection):
    def __init__(self,
            name: str,
            component: Optional[ABCComponent] = None,
            provided_cls: Optional[type] = None,
            provider_cls: Optional[type] = None,
            ) -> None:
        self.provided_cls: Optional[type] = provided_cls
        self.provider_cls: Optional[type] = provider_cls
        self.component: Optional[ABCComponent] = component
        super().__init__(name)

    def set_instance(self, provided_cls: type, provider_cls: type) -> None:
        self.provided_cls = provided_cls
        self.provider_cls = provider_cls

    def set_component(self, component: ABCComponent) -> None:
        self.component = component

    def inject_cls(self) -> Any:
        """Return the provider instance."""
        if self.provided_cls is None or self.provider_cls is None:
            raise DependencyError("ProviderInjection must have provided_cls and provider_cls set before injection.")
        return self.provider_cls(self.provided_cls)
    
    def child_add(self, child: BaseInjection) -> None:
        """ProviderInjection does not support child additions."""
        raise DependencyError("ProviderInjection cannot have children.")

    def child_inject(self) -> Generator['ProviderInjection', None, None]:
        yield self

    def child_wire(self, container: containers.DynamicContainer) -> None:
        """Wire the provider into the provided container."""
        container.wire(modules=[self.component])