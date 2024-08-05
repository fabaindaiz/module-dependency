from dependency_injector.wiring import Provide
from src.container import Container

class Mixin:
    def _wire(self, container):
        return container.wire(modules=[self.__class__])