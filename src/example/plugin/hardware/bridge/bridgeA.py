from dependency.core import instance, providers
from example.plugin.hardware import HardwarePlugin
from example.plugin.hardware.events import EventHardwareOperation
from example.plugin.hardware.bridge import HardwareAbstraction
from example.plugin.hardware.factory import HardwareFactory
from example.plugin.hardware.observer import HardwareObserver

@instance(
    imports=[
        HardwareFactory,
    ],
    provider=providers.Singleton,
)
class HardwareAbstractionBridgeA(HardwareAbstraction):
    def __init__(self) -> None:
        self.__factory: HardwareFactory = HardwareFactory.provide()
        self.__observer: HardwareObserver = HardwareObserver.provide()
        assert HardwarePlugin.config.config == True
        print("AbstractionBridgeA initialized")

    def someOperation(self, product: str) -> None:
        instance = self.__factory.createHardware(product=product)
        instance.doStuff("someOperation")
        self.__observer.update(
            context=EventHardwareOperation(
                product=product,
                operation="someOperation"))

    def otherOperation(self, product: str) -> None:
        instance = self.__factory.createHardware(product=product)
        instance.doStuff("otherOperation")
        self.__observer.update(
            context=EventHardwareOperation(
                product=product,
                operation="otherOperation"))
