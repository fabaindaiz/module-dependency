from dependency_injector import providers
from src.services.singleton.container import SingletonServiceContainer
from src.services.singleton.type1 import Type1SingletonService

class Type1SingletonServiceProvider(SingletonServiceContainer):
    config = providers.Configuration()

    service = providers.Singleton(Type1SingletonService, config)