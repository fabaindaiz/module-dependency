from dependency.core import dependent
from dependency.core.declaration.dependent import Dependent
from example.plugin.reporter.factory.interfaces import Reporter
from example.plugin.hardware.observer import HardwareObserver, HardwareObserverComponent
from example.plugin.hardware.observer.interfaces import EventHardwareCreated, EventHardwareCreatedSubscriber
from example.plugin.hardware.observer.interfaces import EventHardwareOperation, EventHardwareOperationSubscriber

@dependent(
    imports=[
        HardwareObserverComponent
    ]
)
class ReporterA(Reporter, Dependent):
    def __init__(self) -> None:
        self.__observer: HardwareObserver = HardwareObserverComponent.provide()

        self.products: list[str] = []
        self.operations: list[str] = []

        @self.__observer.subscribe(EventHardwareCreatedSubscriber)
        def on_product_created(context: EventHardwareCreated) -> None:
            self.products.append(context.product)

        @self.__observer.subscribe(EventHardwareOperationSubscriber)
        def on_product_operation(context: EventHardwareOperation) -> None:
            self.operations.append(f"{context.product} -> {context.operation}")
    
    def reportProducts(self) -> list[str]:
        return self.products

    def reportOperations(self) -> list[str]:
        return self.operations