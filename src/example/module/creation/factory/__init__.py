from abc import ABC, abstractmethod
from dependency.core import Component, component

class Product(ABC):
    @abstractmethod
    def doStuff(self) -> None:
        pass

@component()
class Creator(ABC, Component):
    def someOperation(self) -> None:
        instance = self.createProduct()
        instance.doStuff()

    @abstractmethod
    def createProduct(self) -> Product:
        pass
