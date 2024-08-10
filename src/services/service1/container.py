from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.dependencies.container import ServiceContainer, Mixin
from src.services.service1 import Service1

class Service1Mixin(Mixin):
    __service1: Service1 = Provide["service1_container.service"]

    @property
    def service1(self) -> Service1:
        return self.__service1

class Service1Container(ServiceContainer):
    name = providers.Object("service1_container")
    inject = providers.Callable(Service1Mixin._wire)