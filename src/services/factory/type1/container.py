from dependency_injector import providers
from src.services.factory.container import FactoryServiceContainer
from src.services.factory.type1 import Type1FactoryService

class Type1FactoryServiceProvider(FactoryServiceContainer):
    config = providers.Configuration()

    service = providers.Factory(Type1FactoryService, config)