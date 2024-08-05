from dependency_injector import containers, providers
from src.service1 import Service1

class Service1Container(containers.DeclarativeContainer):
    service = providers.Singleton(Service1)