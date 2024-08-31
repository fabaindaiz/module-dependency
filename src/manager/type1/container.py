from dependency_injector import providers
from src.manager.container import ManagerContainer
from src.manager.type1 import Type1Manager
from src.services.factory.container import FactoryServiceContainer
from src.services.singleton.container import SingletonServiceContainer

class Type1ManagerProvider(ManagerContainer):
    depends = providers.List(FactoryServiceContainer, SingletonServiceContainer)
    config = providers.Configuration()

    service = providers.Singleton(Type1Manager, config)