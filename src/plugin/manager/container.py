from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.library.dependencies.container import Injectable, ServiceContainer
from src.plugin.manager import Manager

class ManagerMixin(Injectable):
    name = "manager"

    def __init__(self,
            manager: Manager = Provide[f"{name}.service"],
            **kwargs):
        self.__service = manager
        super().__init__(**kwargs)

    @property
    def manager(self) -> Manager:
        return self.__service

class ManagerContainer(ServiceContainer):
    name = providers.Object(ManagerMixin.name)
    inject = providers.Callable(ManagerMixin._wire)