from dependency_injector import providers
from src.services.service1.container import Service1Container
from src.services.service1.instance1 import Service1Instance1
from src.services.service2.container import Service2Container

class Service1Provider(Service1Container):
    depends = providers.List(Service2Container)
    config = providers.Configuration()

    service = providers.Singleton(Service1Instance1, config)