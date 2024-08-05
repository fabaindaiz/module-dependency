from dependency_injector import containers, providers
from src.service1.container import Service1Container
from src.service1.instance1 import Service1Instance1

@containers.override(Service1Container)
class Service1Provider(containers.DeclarativeContainer):
    service = providers.Singleton(Service1Instance1)