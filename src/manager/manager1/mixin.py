from dependency_injector.wiring import Provide
from src.manager.manager1 import Manager1
from src.services.mixin import Mixin
from src.container import Container

class Manager1Mixin(Mixin):
    __service1: Manager1 = Provide[Container.manager1_container.service]

    @property
    def manager1(self) -> Manager1:
        return self.__service1