from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.dependencies.container import ServiceContainer, Mixin
from src.manager.manager1 import Manager1

class Manager1Mixin(Mixin):
    __service1: Manager1 = Provide["manager1_container.service"]

    @property
    def manager1(self) -> Manager1:
        return self.__service1

class Manager1Container(ServiceContainer):
    name = providers.Object("manager1_container")
    inject = providers.Callable(Manager1Mixin._wire)