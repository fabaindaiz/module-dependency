from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.dependencies.container import Injectable, ServiceContainer
from src.services.factory import FactoryService

class FactoryServiceMixin(Injectable):
    def __init__(self, factory_service: FactoryService = Provide["factory_service.service"], **kwargs):
        self.__service = factory_service
        super().__init__(**kwargs)

    @property
    def factory_service(self) -> FactoryService:
        return self.__service

class FactoryServiceContainer(ServiceContainer):
    name = providers.Object("factory_service")
    inject = providers.Callable(FactoryServiceMixin._wire)