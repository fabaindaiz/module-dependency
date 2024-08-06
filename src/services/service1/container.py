from dependency_injector import providers
from src.services.container import ServiceContainer
from src.services.service1 import Service1

class Service1Container(ServiceContainer):
    service = providers.Singleton(Service1)