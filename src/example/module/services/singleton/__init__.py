from abc import ABC, abstractmethod
from dependency.core import Component, component

class Singleton(ABC):
    @abstractmethod
    def work(self) -> None:
        pass

@component(
    interface=Singleton
)
class SingletonMixin(Component):
    pass