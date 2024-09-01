from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.dependencies.container import Injectable, ServiceContainer
from src.services.singleton import SingletonService

class SingletonServiceMixin(Injectable):
    def __init__(self, singleton_service: SingletonService = Provide["singleton_service.service"], **kwargs):
        self.__service = singleton_service
        super().__init__(**kwargs)

    @property
    def singleton_service(self) -> SingletonService:
        return self.__service

class SingletonServiceContainer(ServiceContainer):
    name = providers.Object("singleton_service")
    inject = providers.Callable(SingletonServiceMixin._wire)