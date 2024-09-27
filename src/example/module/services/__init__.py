from dependency.core import ProviderModule, module
from example.module.services.factory import FactoryComponent
from example.module.services.singleton import SingletonComponent
from example.module.services.factory.type1 import Type1Factory
from example.module.services.singleton.type1 import Type1Singleton

@module(
    declaration=[
        FactoryComponent,
        SingletonComponent,
    ],
    bootstrap=[
        SingletonComponent
    ]
)
class Services(ProviderModule):
    def declare_providers(self): # type: ignore
        return [
            Type1Factory,
            Type1Singleton
        ]