from dependency_injector.wiring import Provide, inject
from src.container import Container
from src.service1 import Service1

class Service1Mixin:
    @property
    @inject
    def service1(self, _service1: Service1 = Provide[Container.service1_container.service]) -> Service1:
        return _service1
    
    @staticmethod
    def _wire(container):
        return container.wire(modules=[__name__])