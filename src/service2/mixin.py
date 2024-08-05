from dependency_injector.wiring import Provide, inject
from src.service2 import Service2
from src.container import Container
from src.mixin import Mixin

class Service2Mixin(Mixin):
    __service2: Service2 = Provide[Container.service2_container.service]

    @property
    def service2(self) -> Service2:
        return self.__service2