from dependency_injector import containers, providers
from src.service2.container import Service2Provider
from src.service2.instance import Service2Instance

@containers.override(Service2Provider)
class Service2InstanceProvider(containers.DeclarativeContainer):
    service = providers.Singleton(Service2Instance)