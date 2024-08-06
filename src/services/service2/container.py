from dependency_injector import providers
from src.services.container import ServiceContainer
from src.services.service2 import Service2

class Service2Container(ServiceContainer):
    service = providers.Singleton(Service2)