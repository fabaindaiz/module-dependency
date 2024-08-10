from dependency_injector.wiring import Provide
from src.services.service1 import Service1
from src.services.mixin import Mixin

class Service1Mixin(Mixin):
    __service1: Service1 = Provide["service1_container.service"]

    @property
    def service1(self) -> Service1:
        return self.__service1