from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugins.hardware.factory.interfaces import Hardware

class HardwareFactory(ABC):
    @abstractmethod
    def createHardware(self, product: str) -> Hardware:
        pass

    def createHardwares1(self, products: list[str]) -> list[Hardware]:
        return [self.createHardware(product) for product in products]

@component(
    interface=HardwareFactory
)
class HardwareFactoryComponent(Component):
    pass