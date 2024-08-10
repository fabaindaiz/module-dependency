from dependency_injector import providers
from src.services.container import ServiceContainer
from src.services.service1 import Service1

class Service1Container(ServiceContainer):
    name = providers.Object("service1_container")
    service = providers.Singleton(Service1)