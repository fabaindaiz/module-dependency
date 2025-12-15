from abc import ABC, abstractmethod
from typing import Any, Generator, Optional
from dependency_injector import containers
from dependency.core2.injection.injectable import Injectable

class BaseInjection(ABC):
    def __init__(self,
        name: str,
        parent: Optional["ContainerInjection"] = None
    ) -> None:
        self.name = name
        self.parent = parent

        if parent:
            parent.childs.append(self)

    @property
    def reference(self) -> str:
        """Return the reference for dependency injection."""
        if not self.parent:
            return self.name
        return f"{self.parent.reference}.{self.name}"

    @abstractmethod
    def inject_cls(self) -> Any:
        """Return the class to be injected."""
        pass

    @abstractmethod
    def resolve_providers(self) -> Generator[Injectable, None, None]:
        """Inject all children into the current injection context."""
        pass

    def __repr__(self) -> str:
        return self.name

class ContainerInjection(BaseInjection):
    def __init__(self,
        name: str,
        parent: Optional["ContainerInjection"] = None
    ) -> None:
        super().__init__(name=name, parent=parent)
        self.childs: list[BaseInjection] = []
        self.container = containers.DynamicContainer()

    def inject_cls(self) -> containers.DynamicContainer:
        """Return the container instance."""
        return self.container

    def resolve_providers(self) -> Generator[Injectable, None, None]:
        for child in self.childs:
            setattr(self.container, child.name, child.inject_cls())
            yield from child.resolve_providers()
