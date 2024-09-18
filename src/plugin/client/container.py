from dependency_injector import providers
from dependency_injector.wiring import Provide
from src.library.dependencies.container import Injectable, ServiceContainer
from src.plugin.client import Client

class ClientMixin(Injectable):
    name = "client"

    def __init__(self,
            client: Client = Provide[f"{name}.service"],
            **kwargs):
        self.__service = client
        super().__init__(**kwargs)

    @property
    def client(self) -> Client:
        return self.__service

class ClientContainer(ServiceContainer):
    name = providers.Object(ClientMixin.name)
    inject = providers.Callable(ClientMixin._wire)
    start = providers.Resource(ClientMixin)