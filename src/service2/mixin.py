from dependency_injector.wiring import Provide, inject
from src.container import Container
from src.service2 import Service2

class Service2Mixin:
    @property
    @inject
    def service2(self, _service2: Service2 = Provide[Container.service2_container.service]) -> Service2:
        return _service2
    
    @staticmethod
    def _wire(container):
        return container.wire(modules=[__name__])