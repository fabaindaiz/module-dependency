from dependency.core import provider, providers
from example.plugins.hardware.factory import HardwareFactory, HardwareFactoryComponent
from example.plugins.hardware.factory.interfaces import Hardware
from example.plugins.hardware.factory.products.productB import HardwareB
from example.plugins.hardware.factory.products.productC import HardwareC
from example.plugins.hardware.observer import HardwareObserver, HardwareObserverComponent
from example.plugins.hardware.observer.interfaces import EventHardwareCreated

@provider(
    component=HardwareFactoryComponent,
    imports=[
        HardwareObserverComponent
    ],
    dependents=[
        HardwareB,
        HardwareC
    ],
    provider = providers.Singleton
)
class HardwareFactoryCreatorB(HardwareFactory):
    def __init__(self, config: dict):
        self.__observer: HardwareObserver = HardwareObserverComponent()
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