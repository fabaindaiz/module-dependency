from dependency.core import Product, product, providers
from example.plugin.reporter.interfaces import Reporter
from example.plugin.hardware.events import EventSubscriber, EventHardwareCreated, EventHardwareOperation
from example.plugin.hardware.observer import HardwareObserver

@product(
    imports=[
        HardwareObserver,
    ],
    provider=providers.Factory,
)
class ReporterA(Reporter, Product):
    def __init__(self) -> None:
        self.__observer: HardwareObserver = HardwareObserver.provide()

        self.products: list[str] = []
        self.operations: list[str] = []

        @self.__observer.subscribe(EventSubscriber) # type: ignore
        def on_product_created(context: EventHardwareCreated) -> None:
            self.products.append(context.product)

        @self.__observer.subscribe(EventSubscriber) # type: ignore
        def on_product_operation(context: EventHardwareOperation) -> None:
            self.operations.append(f"{context.product} -> {context.operation}")

    def reportProducts(self) -> list[str]:
        return self.products

    def reportOperations(self) -> list[str]:
        return self.operations
