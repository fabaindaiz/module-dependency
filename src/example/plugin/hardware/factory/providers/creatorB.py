from dependency.core import instance, providers
from example.plugin.hardware.interfaces import Hardware
from example.plugin.hardware.events import EventHardwareCreated
from example.plugin.hardware.factory import HardwareFactory
from example.plugin.hardware.factory.products.productB import HardwareB
from example.plugin.hardware.factory.products.productC import HardwareC
from example.plugin.hardware.observer import HardwareObserver

@instance(
    imports=[
        HardwareObserver,
    ],
    products=[
        HardwareB,
        HardwareC
    ],
    provider=providers.Singleton,
)
class HardwareFactoryCreatorB(HardwareFactory):
    def __init__(self):
        self.__observer: HardwareObserver = HardwareObserver.provide()
        print("FactoryCreatorB initialized")

    def createProduct(self, product: str) -> Hardware:
        match product:
            case "B":
                self.__observer.update(
                    context=EventHardwareCreated(product="B"))
                return HardwareB()
            case "C":
                self.__observer.update(
                    context=EventHardwareCreated(product="C"))
                return HardwareC()
            case _:
                raise ValueError(f"Unknown product type: {product}")
