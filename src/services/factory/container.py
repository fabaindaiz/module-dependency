from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.library.dependencies.container import Injectable, ServiceContainer
from src.services.factory import FactoryService

class FactoryServiceMixin(Injectable):
    name = "factory_service"
    
    def __init__(self,
            factory_service: FactoryService = Provide[f"{name}.service"],
            **kwargs):
        self.__service = factory_service
        super().__init__(**kwargs)

    @property
    def factory_service(self) -> FactoryService:
        return self.__service

class FactoryServiceContainer(ServiceContainer):
    name = providers.Object(FactoryServiceMixin.name)
    inject = providers.Callable(FactoryServiceMixin._wire)