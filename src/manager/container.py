from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.dependencies.container import ServiceContainer, Mixin
from src.manager import Manager

class ManagerMixin(Mixin):
    __service: Manager = Provide["manager.service"]

    @property
    def manager(self) -> Manager:
        return self.__service

class ManagerContainer(ServiceContainer):
    name = providers.Object("manager")
    inject = providers.Callable(ManagerMixin._wire)