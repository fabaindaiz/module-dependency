from dependency_injector.wiring import Provide
from src.container import Container

class Mixin:
    __config = Provide[Container.config]

    def _init(self, service):
        service.init(self.__config)

    def _wire(self, container):
        return container.wire(modules=[self.__class__])