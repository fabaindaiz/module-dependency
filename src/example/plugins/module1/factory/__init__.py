from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugins.module1.factory.interfaces import Product

class Creator(ABC):
    @abstractmethod
    def createProduct(self, product: str) -> Product:
        pass

    def someOperation(self, product: str) -> None:
        instance = self.createProduct(product=product)
        instance.doStuff()

@component(
    interface=Creator
)
class CreatorComponent(Component):
    pass