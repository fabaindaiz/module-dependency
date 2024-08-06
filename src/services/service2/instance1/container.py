from dependency_injector import providers
from src.services.service2.container import Service2Container
from src.services.service2.instance1 import Service2Instance1
from src.services.service2.mixin import Service2Mixin

class Service2Provider(Service2Container):
    config = providers.Configuration()
    inject = providers.Callable(Service2Mixin._wire)

    service = providers.Singleton(Service2Instance1, config)