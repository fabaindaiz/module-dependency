from dependency_injector.wiring import Provide, inject
from src.services.service2 import Service2
from src.services.mixin import Mixin
from src.container import Container

class Service2Mixin(Mixin):
    __service2: Service2 = Provide[Container.service2_container.service]

    @property
    def service2(self) -> Service2:
        return self.__service2