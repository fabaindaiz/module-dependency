from dependency.core import HasDependent,  provider, providers
from example.plugin.hardware.factory import HardwareFactory, HardwareFactoryComponent
from example.plugin.hardware.factory.interfaces import Hardware
from example.plugin.hardware.factory.products.productA import HardwareA
from example.plugin.hardware.factory.products.productB import HardwareB
from example.plugin.hardware.observer import HardwareObserver, HardwareObserverComponent
from example.plugin.hardware.observer.interfaces import EventHardwareCreated

@provider(
    component=HardwareFactoryComponent,
    imports=[
        HardwareObserverComponent
    ],
    dependents=[
        HardwareA,
        HardwareB,
    ],
    provider = providers.Singleton
)
class HardwareFactoryCreatorA(HardwareFactory, HasDependent):
    def __init__(self, config: dict):
        self.__observer: HardwareObserver = HardwareObserverComponent.provide()
        print("FactoryCreatorA initialized")

    def createHardware(self, product: str) -> Hardware:
        instance: Hardware
        match product:
            case "A":
                self.declare_dependents([HardwareA])
                instance = HardwareA()
                self.__observer.update(
                    context=EventHardwareCreated(product="A"))
                return instance
            case "B":
                self.declare_dependents([HardwareB])
                instance = HardwareB()
                self.__observer.update(
                    context=EventHardwareCreated(product="B"))
                return instance
            case _:
                raise ValueError(f"Unknown product type: {product}")