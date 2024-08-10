from dependency_injector.wiring import Provide
from src.services.service2 import Service2
from src.services.mixin import Mixin

class Service2Mixin(Mixin):
    __service2: Service2 = Provide["service2_container.service"]

    @property
    def service2(self) -> Service2:
        return self.__service2