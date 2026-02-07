from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugin.hardware import HardwarePlugin
from example.plugin.hardware.interfaces import Hardware

@component(
    module=HardwarePlugin,
)
class HardwareFactory(ABC, Component):
    @abstractmethod
    def createHardware(self, product: str) -> Hardware:
        pass

    def createHardwares1(self, products: list[str]) -> list[Hardware]:
        return [self.createHardware(product) for product in products]
