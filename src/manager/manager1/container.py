from dependency_injector import providers
from src.services.container import ServiceContainer
from src.manager.manager1 import Manager1

class Manager1Container(ServiceContainer):
    service = providers.Singleton(Manager1)