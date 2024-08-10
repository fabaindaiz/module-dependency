from dependency_injector import providers
from src.services.container import ServiceContainer
from src.services.service2 import Service2

class Service2Container(ServiceContainer):
    name = providers.Object("service2_container")
    service = providers.Singleton(Service2)