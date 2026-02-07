from dependency.core import instance, providers
from example.plugin.hardware.interfaces import Hardware
from example.plugin.hardware.factory import HardwareFactory
from example.plugin.hardware.factory.products.productA import HardwareA
from example.plugin.hardware.factory.products.productB import HardwareB
from example.plugin.hardware.observer import HardwareObserver
from example.plugin.hardware.events import EventHardwareCreated

@instance(
    component=HardwareFactory,
    imports=[
        HardwareObserver,
    ],
    products=[
        HardwareA,
        HardwareB,
    ],
    provider=providers.Singleton,
)
class HardwareFactoryCreatorA(HardwareFactory):
    def __init__(self):
        self.__observer: HardwareObserver = HardwareObserver.provide()
        print("FactoryCreatorA initialized")

    def createHardware(self, product: str) -> Hardware:
        instance: Hardware
        match product:
            case "A":
                instance = HardwareA()
                self.__observer.update(
                    context=EventHardwareCreated(product="A"))
                return instance
            case "B":
                instance = HardwareB()
                self.__observer.update(
                    context=EventHardwareCreated(product="B"))
                return instance
            case _:
                raise ValueError(f"Unknown product type: {product}")
