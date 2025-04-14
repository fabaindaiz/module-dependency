from dependency.core import provider, providers
from example.plugins.module1.facade import Facade, FacadeComponent
from example.plugins.module1.bridge import Abstraction, AbstractionComponent
from example.plugins.module1.factory.interfaces import Product
from example.plugins.module1.observer import Observer, ObserverComponent
from example.plugins.module1.observer.interfaces import EventProductCreated, EventProductCreatedSubscriber
from example.plugins.module1.observer.interfaces import EventProductOperation, EventProductOperationSubscriber

@provider(
    component=FacadeComponent,
    imports=[
        AbstractionComponent,
        ObserverComponent
    ],
    provider = providers.Singleton
)
class FacadeA(Facade):
    def __init__(self, config: dict) -> None:
        self.__bridge: Abstraction = AbstractionComponent.provide()
        self.__observer: Observer = ObserverComponent.provide()

        self.products: list[str] = []
        self.operations: list[str] = []

        @self.__observer.subscribe(EventProductCreatedSubscriber)
        def on_product_created(context: EventProductCreated) -> None:
            self.products.append(context.product)

        @self.__observer.subscribe(EventProductOperationSubscriber)
        def on_product_operation(context: EventProductOperation) -> None:
            self.operations.append(f"{context.product} -> {context.operation}")
        
        self.startModule()
        print("FacadeA initialized")

    def startModule(self) -> None:
        self.__bridge.someOperation(product="A")
        self.__bridge.otherOperation(product="B")
        print("reportProducts:", self.reportProducts())
        print("reportOperations:", self.reportOperations())

    def reportProducts(self) -> list[str]:
        return self.products

    def reportOperations(self) -> list[str]:
        return self.operations
