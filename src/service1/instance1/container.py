from dependency_injector import containers, providers
from src.service1.container import Service1Container
from src.service1.instance1 import Service1Instance1
from src.service1.mixin import Service1Mixin

@containers.override(Service1Container)
class Service1Provider(containers.DeclarativeContainer):
    config = providers.Configuration()
    service = providers.Singleton(Service1Instance1, config)
    inject = providers.Callable(Service1Mixin._wire)