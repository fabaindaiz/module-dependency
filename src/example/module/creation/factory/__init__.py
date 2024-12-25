from abc import ABC, abstractmethod
from dependency.core import Component, component

class FactoryInterface(ABC):
    @abstractmethod
    def work(self) -> None:
        pass

class Factory(ABC):
    def work(self) -> None:
        instance = self.create()
        instance.work()

    @abstractmethod
    def create(self) -> FactoryInterface:
        pass

@component(
    interface=Factory
)
class FactoryComponent(Component):
    pass