from abc import ABC, abstractmethod
from dependency_injector import containers, providers

class Injectable(ABC):
    def __init__(self, *args, **kwargs) -> None:
        if len(args) > 0:
            raise ValueError("Providers Constructor must receive cfg as a keyword argument")
        super().__init__()

    @classmethod
    def _wire(cls, container: containers.Container):
        return container.wire(modules=[cls])

class ServiceContainer(containers.DeclarativeContainer):
    name = providers.Object()
    depends = providers.List()
    config = providers.Configuration()
    inject = providers.Callable(containers.DeclarativeContainer)