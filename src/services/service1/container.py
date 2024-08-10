from dependency_injector import providers
from src.services.container import ServiceContainer
from src.services.service1.mixin import Service1Mixin

class Service1Container(ServiceContainer):
    name = providers.Object("service1_container")
    inject = providers.Callable(Service1Mixin._wire)