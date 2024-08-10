from dependency_injector import providers
from src.services.container import ServiceContainer
from src.services.service2.mixin import Service2Mixin

class Service2Container(ServiceContainer):
    name = providers.Object("service2_container")
    inject = providers.Callable(Service2Mixin._wire)