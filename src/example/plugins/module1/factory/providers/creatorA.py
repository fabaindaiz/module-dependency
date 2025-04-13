from dependency.core import provider, providers
from example.plugins.module1.factory import Factory, FactoryComponent
from example.plugins.module1.factory.interfaces import Product
from example.plugins.module1.factory.products.productA import ProductA
from example.plugins.module1.factory.products.productB import ProductB
from example.plugins.module1.observer import Observer, ObserverComponent
from example.plugins.module1.observer.interfaces import EventProductCreated

@provider(
    component=FactoryComponent,
    imports=[
        ObserverComponent
    ],
    dependents=[
        ProductA,
        ProductB
    ],
    provider = providers.Singleton
)
class FactoryCreatorA(Factory):
    def __init__(self, config: dict):
        self.__observer: Observer = ObserverComponent.provide()
        print("FactoryCreatorA initialized")

    def createProduct(self, product: str) -> Product:
        match product:
            case "A":
                instance = ProductA()
                self.__observer.update(
                    context=EventProductCreated(product="A"))
                return instance
            case "B":
                instance = ProductB()
                self.__observer.update(
                    context=EventProductCreated(product="B"))
                return instance
            case _:
                raise ValueError(f"Unknown product type: {product}")