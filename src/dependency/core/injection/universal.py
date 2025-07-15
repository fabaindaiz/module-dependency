from abc import ABC, abstractmethod
from dependency_injector import containers, providers
from typing import Any, Callable, Optional

class InjectionError(Exception): ...

class BaseInjection(ABC):
    def __init__(self,
            name: str
            ) -> None:
        self.__parent: Optional["BaseInjection"] = None
        self.name: str = name
    
    @property
    def parent(self) -> Optional["BaseInjection"]:
        return self.__parent
    
    @parent.setter
    def parent(self, value: "BaseInjection"):
        if self.__parent is not None:
            raise InjectionError("Parent can only be set once.")
        self.__parent = value
    
    def reference(self) -> str:
        if self.parent:
            return f"{self.parent.reference()}.{self.name}"
        return self.name
    
    @abstractmethod
    def inject_cls(self) -> Any:
        """Return the class to be injected."""
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    @abstractmethod
    def inject_child(self, child: "BaseInjection") -> None:
        """Inject a child into the current injection context."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abstractmethod
    def wire(self, container: containers.DynamicContainer) -> None:
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
    
    def inject_child(self, child: BaseInjection) -> None:
        self.__childs.append(child)
        setattr(self.container, child.name, child.inject_cls())
        child.parent = self

    def wire(self, container: containers.DynamicContainer) -> None:
        """Wire the container with the current injection context."""
        for child in self.__childs:
            child.wire(container)

class ProviderInjection(BaseInjection):
    def __init__(self,
            name: str,
            provided_cls: type,
            provider_cls: type,
            wire_cls: type,
            ) -> None:
        self.provided_cls = provided_cls
        self.provider_cls = provider_cls
        self.wire_cls = wire_cls
        super().__init__(name)
    
    def inject_cls(self) -> Any:
        """Return the provider instance."""
        return self.provider_cls(self.provided_cls)
    
    def inject_child(self, child: BaseInjection) -> None:
        raise InjectionError("ProviderInjection cannot have children.")
    
    def wire(self, container: containers.DynamicContainer) -> None:
        """Wire the provider into the provided container."""
        if not isinstance(self.wire_cls, type):
            raise InjectionError("wire_cls must be a type.")
        setattr(container, self.name, self.wire_cls(self.provider_cls(self.provided_cls)))
        #container.wire(modules=[self.wire_cls])