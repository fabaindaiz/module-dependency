from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugin.hardware import HardwarePlugin

@component(
    module=HardwarePlugin,
)
class HardwareAbstraction(ABC, Component):
    @abstractmethod
    def someOperation(self, product: str) -> None:
        pass

    @abstractmethod
    def otherOperation(self, product: str) -> None:
        pass
