from dependency_injector import containers, providers
from src.service1.container import Service1Provider
from src.service1.instance import Service1Instance

@containers.override(Service1Provider)
class Service1InstanceProvider(containers.DeclarativeContainer):
    service = providers.Singleton(Service1Instance)