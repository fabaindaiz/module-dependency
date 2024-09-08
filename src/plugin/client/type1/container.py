from dependency_injector import providers
from src.services.factory.container import FactoryServiceContainer
from src.services.singleton.container import SingletonServiceContainer
from src.plugin.client.container import ClientContainer
from src.plugin.client.type1 import Type1Client

class Type1ClientProvider(ClientContainer):
    depends = providers.List(FactoryServiceContainer, SingletonServiceContainer)
    config = providers.Configuration()

    service = providers.Singleton(Type1Client, config)