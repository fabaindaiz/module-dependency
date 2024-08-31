from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.dependencies.container import ServiceContainer, Mixin
from src.services.singleton import SingletonService

class SingletonServiceMixin(Mixin):
    __service: SingletonService = Provide["singleton_service.service"]

    @property
    def singleton_service(self) -> SingletonService:
        return self.__service

class SingletonServiceContainer(ServiceContainer):
    name = providers.Object("singleton_service")
    inject = providers.Callable(SingletonServiceMixin._wire)