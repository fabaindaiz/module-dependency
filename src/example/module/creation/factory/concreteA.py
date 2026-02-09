from dependency.core import instance, providers
from example.module.creation.factory import Creator, Product

class ConcreteProductA(Product):
    def doStuff(self) -> None:
        print("ConcreteProductA works")

@instance(
    provider=providers.Factory,
)
class ConcreteCreatorA(Creator):
    def createProduct(self) -> ConcreteProductA:
        return ConcreteProductA()
