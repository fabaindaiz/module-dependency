from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugins.module1.factory.interfaces import Product

class Factory(ABC):
    @abstractmethod
    def createProduct(self, product: str) -> Product:
        pass

    def createProducts(self, products: list[str]) -> list[Product]:
        return [self.createProduct(product) for product in products]

@component(
    interface=Factory
)
class FactoryComponent(Component):
    pass