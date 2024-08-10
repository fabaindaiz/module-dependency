from dependency_injector import providers
from src.services.service2.container import Service2Container
from src.services.service2.instance1 import Service2Instance1

class Service2Provider(Service2Container):
    config = providers.Configuration()

    service = providers.Singleton(Service2Instance1, config)