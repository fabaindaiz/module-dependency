from dependency_injector import providers
from src.plugin.client.type1 import Type1Client
from src.plugin.client.container import ClientContainer
from src.plugin.manager.container import ManagerContainer

class Type1ClientProvider(ClientContainer):
    depends = providers.List(ManagerContainer)
    config = providers.Configuration()

    service = providers.Singleton(Type1Client, config)