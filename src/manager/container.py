from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.dependencies.container import Injectable, ServiceContainer
from src.manager import Manager

class ManagerMixin(Injectable):
    def __init__(self, manager: Manager = Provide["manager.service"], **kwargs):
        self.__service = manager
        super().__init__()

    @property
    def manager(self) -> Manager:
        return self.__service

class ManagerContainer(ServiceContainer):
    name = providers.Object("manager")
    inject = providers.Callable(ManagerMixin._wire)