from abc import ABC, abstractmethod
from dependency.core.declaration.component import Component, component
from example.plugins.common import CommonModule

class StorageService(ABC):
    @abstractmethod
    def get(self, key: str) -> str:
        """Retrieve a value by key."""
        pass

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        """Set a value by key."""
        pass

@component(
    module=CommonModule,
    interface=StorageService
)
class StorageServiceComponent(Component):
    pass