from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugin.hardware import HardwarePlugin

@component(
    module=HardwarePlugin,
)
class HardwareAbstraction(Component):
    @abstractmethod
    def someOperation(self, product: str) -> None:
        pass

    @abstractmethod
    def otherOperation(self, product: str) -> None:
        pass
