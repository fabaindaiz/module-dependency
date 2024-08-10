from dependency_injector import providers
from src.services.container import ServiceContainer
from src.manager.manager1.mixin import Manager1Mixin

class Manager1Container(ServiceContainer):
    name = providers.Object("manager1_container")
    inject = providers.Callable(Manager1Mixin._wire)