from dependency.core import ProviderModule, module
from example.plugins.module1.bridge import AbstractionComponent
from example.plugins.module1.factory import FactoryComponent
from example.plugins.module1.observer import ObserverComponent
from example.plugins.module1.facade import FacadeComponent

@module(
    declaration=[
        AbstractionComponent,
        FactoryComponent,
        ObserverComponent,
        FacadeComponent
    ],
    bootstrap=[
        FacadeComponent
    ]
)
class Module1(ProviderModule):
    def declare_providers(self):
        # Common providers
        from example.plugins.module1.bridge.providers.bridgeA import AbstractionBridgeA
        from example.plugins.module1.factory.providers.creatorA import FactoryCreatorA
        from example.plugins.module1.observer.providers.publisherA import PublisherObserverA
        from example.plugins.module1.facade.providers.facadeA import FacadeA
        return [
            AbstractionBridgeA,
            FactoryCreatorA,
            PublisherObserverA,
            FacadeA
        ]