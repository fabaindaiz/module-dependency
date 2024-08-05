from dependency_injector import providers
from src.service1.container import Service1Container
from src.service1.instance1 import Service1Instance1
from src.service1.mixin import Service1Mixin

class Service1Provider(Service1Container):
    config = providers.Configuration()
    inject = providers.Callable(Service1Mixin._wire)

    service = providers.Singleton(Service1Instance1, config)