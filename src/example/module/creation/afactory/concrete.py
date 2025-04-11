from dependency.core import dependent, provider, Provider, providers
from example.module.creation.afactory import Creator, CreatorComponent, Product
from example.module.creation.factory import CreatorComponent as a

@dependent(
    imports=[a],
)
class ConcreteProductA(Product):
    def doStuff(self) -> None:
        print("ConcreteProductA works")

@dependent()
class ConcreteProductB(Product):
    def doStuff(self) -> None:
        print("ConcreteProductB works")


@provider(
    component=CreatorComponent,
    dependents=[
        ConcreteProductA,
        ConcreteProductB
    ],
)
class ConcreteCreator(Creator):
    def __init__(self, config: dict) -> None:
        super().__init__()
        self.__local: Product = self.createProduct("A")
        self.__local.doStuff()

    def createProduct(self, type: str) -> Product:
        match type:
            case "A":
                return ConcreteProductA()
            case "B":
                return ConcreteProductB()