from dependency_injector import providers
from src.services.container import ServiceContainer
from src.manager.manager1 import Manager1

class Manager1Container(ServiceContainer):
    name = providers.Object("manager1_container")
    service = providers.Singleton(Manager1)