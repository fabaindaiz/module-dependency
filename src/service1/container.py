from dependency_injector import containers, providers
from src.service1 import Service1

class Service1Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    service = providers.Singleton(Service1)
    inject = providers.Dependency()