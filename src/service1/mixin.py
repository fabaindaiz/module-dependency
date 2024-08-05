from dependency_injector.wiring import Provide, inject
from src.container import Container
from src.service1 import Service1

class Service1Mixin:
    _service1: Service1 = Provide[Container.service1_container.service]

    @property
    def service1(self) -> Service1:
        return self._service1
    
    @staticmethod
    def _wire(container):
        return container.wire(modules=[Service1Mixin])