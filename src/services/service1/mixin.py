from dependency_injector.wiring import Provide, inject
from src.services.service1 import Service1
from src.services.mixin import Mixin
from src.container import Container

class Service1Mixin(Mixin):
    __service1: Service1 = Provide[Container.service1_container.service]

    @property
    def service1(self) -> Service1:
        return self.__service1