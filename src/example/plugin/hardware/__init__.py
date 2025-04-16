from dependency.core import Module, module
from example.plugin.hardware.bridge import HardwareAbstractionComponent
from example.plugin.hardware.factory import HardwareFactoryComponent
from example.plugin.hardware.observer import HardwareObserverComponent

@module(
    declaration=[
        HardwareAbstractionComponent,
        HardwareFactoryComponent,
        HardwareObserverComponent,
    ]
)
class HardwareModule(Module):
    def declare_providers(self):
        # Common providers
        from example.plugin.hardware.bridge.providers.bridgeA import HardwareAbstractionBridgeA
        from example.plugin.hardware.factory.providers.creatorA import HardwareFactoryCreatorA
        from example.plugin.hardware.observer.providers.publisherA import HardwareObserverA