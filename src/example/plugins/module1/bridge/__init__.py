from abc import ABC, abstractmethod
from dependency.core import Component, component

class Abstraction(ABC):
    @abstractmethod
    def someOperation(self, product: str) -> None:
        pass

    @abstractmethod
    def otherOperation(self, product: str) -> None:
        pass

@component(
    interface=Abstraction
)
class AbstractionComponent(Component):
    pass