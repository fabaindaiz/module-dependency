from dependency_injector import containers, providers
from src.service2.container import Service2Container
from src.service2.instance1 import Service2Instance1
from src.service2.mixin import Service2Mixin

@containers.override(Service2Container)
class Service2Provider(containers.DeclarativeContainer):
    config = providers.Configuration()
    service = providers.Singleton(Service2Instance1, config)
    inject = providers.Callable(Service2Mixin._wire)