from dependency_injector import providers
from src.service2 import Service2
from src.service import ServiceContainer

class Service2Container(ServiceContainer):
    service = providers.Singleton(Service2)