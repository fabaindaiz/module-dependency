from dependency_injector.wiring import Provide, inject
from src.service1 import Service1
from src.container import Container
from src.mixin import Mixin

class Service1Mixin(Mixin):
    _service1: Service1 = Provide[Container.service1_container.service]

    @property
    def service1(self) -> Service1:
        return self._service1