from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.dependencies.container import ServiceContainer, Mixin
from src.dependencies.injection import Injectable, use_injection
from src.services.factory import FactoryService

class FactoryServiceMixin(Mixin, Injectable):
    def _make_injection(self, factory_service: FactoryService = Provide["factory_service.service"]):
        self.__service = factory_service

    @property
    @use_injection
    def factory_service(self) -> FactoryService:
        return self.__service

class FactoryServiceContainer(ServiceContainer):
    name = providers.Object("factory_service")
    inject = providers.Callable(FactoryServiceMixin._wire)