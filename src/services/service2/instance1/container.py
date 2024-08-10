from dependency_injector import providers
from src.services.service2.container import Service2Container
from src.services.service2.instance1 import Service2Instance1
from src.services.service1.container import Service1Container

class Service2Provider(Service2Container):
    depends = providers.List(Service1Container)
    config = providers.Configuration()

    service = providers.Singleton(Service2Instance1, config)