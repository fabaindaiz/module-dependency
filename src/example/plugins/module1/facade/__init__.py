from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugins.module1.factory.interfaces import Product

class Facade(ABC):
    @abstractmethod
    def startModule(self) -> None:
        pass

    @abstractmethod
    def reportProducts(self) -> list[str]:
        pass

    @abstractmethod
    def reportOperations(self) -> list[str]:
        pass

@component(
    interface=Facade
)
class FacadeComponent(Component):
    pass