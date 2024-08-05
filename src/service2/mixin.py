from dependency_injector.wiring import Provide, inject
from src.container import Container
from src.service2 import Service2

class Service2Mixin:
    _service2: Service2 = Provide[Container.service2_container.service]

    @property
    def service2(self) -> Service2:
        return self._service2
    
    @staticmethod
    def _wire(container):
        return container.wire(modules=[Service2Mixin])