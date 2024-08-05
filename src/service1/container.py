from dependency_injector import providers
from src.service import ServiceContainer
from src.service1 import Service1

class Service1Container(ServiceContainer):
    service = providers.Singleton(Service1)