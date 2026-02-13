from dependency.core import instance, providers
from example.module.creation.factory import Creator, Product

class ConcreteProductB(Product):
    def doStuff(self) -> None:
        print("ConcreteProductA works")

@instance(
    provider=providers.Factory,
)
class ConcreteCreatorB(Creator):
    def createProduct(self) -> ConcreteProductB:
        return ConcreteProductB()
