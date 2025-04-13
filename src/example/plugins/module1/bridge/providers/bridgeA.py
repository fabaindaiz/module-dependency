from dependency.core import provider, providers
from example.plugins.module1.bridge import Abstraction, AbstractionComponent
from example.plugins.module1.factory import Factory, FactoryComponent
from example.plugins.module1.observer import Observer, ObserverComponent
from example.plugins.module1.observer.interfaces import EventProductOperation

@provider(
    component=AbstractionComponent,
    imports=[
        FactoryComponent
    ],
    provider = providers.Singleton
)
class AbstractionBridgeA(Abstraction):
    def __init__(self, config: dict) -> None:
        self.__factory: Factory = FactoryComponent.provide()
        self.__observer: Observer = ObserverComponent.provide()
        print("AbstractionBridgeA initialized")

    def someOperation(self, product: str) -> None:
        instance = self.__factory.createProduct(product=product)
        instance.doStuff("someOperation")
        self.__observer.update(
            context=EventProductOperation(product=product, operation="someOperation"))

    def otherOperation(self, product: str) -> None:
        instance = self.__factory.createProduct(product=product)
        instance.doStuff("otherOperation")
        self.__observer.update(
            context=EventProductOperation(product=product, operation="otherOperation"))