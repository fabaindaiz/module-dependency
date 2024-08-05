from dependency_injector import containers, providers
from src.service2.container import Service2Container
from src.service2.instance1 import Service2Instance1

@containers.override(Service2Container)
class Service2Provider(containers.DeclarativeContainer):
    service = providers.Singleton(Service2Instance1)