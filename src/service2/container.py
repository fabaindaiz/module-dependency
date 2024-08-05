from dependency_injector import containers, providers
from src.service2 import Service2

class Service2Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    service = providers.Singleton(Service2)
    inject = providers.Dependency()