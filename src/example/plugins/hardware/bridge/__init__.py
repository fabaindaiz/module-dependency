from abc import ABC, abstractmethod
from dependency.core import Component, component

class HardwareAbstraction(ABC):
    @abstractmethod
    def someOperation(self, product: str) -> None:
        pass

    @abstractmethod
    def otherOperation(self, product: str) -> None:
        pass

@component(
    interface=HardwareAbstraction
)
class HardwareAbstractionComponent(Component):
    pass