from abc import ABC, abstractmethod
from dependency.core.declaration import Component, component
from example.plugins.base.settings import BasePluginConfig

class CacheService(ABC):
    @abstractmethod
    def get(self, key: str) -> str:
        raise NotImplementedError("This method should be overridden in subclasses")

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        raise NotImplementedError("This method should be overridden in subclasses")

@component(
    interface=CacheService
)
class CacheServiceComponent(Component):
    pass