from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.dependencies.container import ServiceContainer, Mixin
from src.services.service2 import Service2

class Service2Mixin(Mixin):
    __service2: Service2 = Provide["service2_container.service"]

    @property
    def service2(self) -> Service2:
        return self.__service2

class Service2Container(ServiceContainer):
    name = providers.Object("service2_container")
    inject = providers.Callable(Service2Mixin._wire)