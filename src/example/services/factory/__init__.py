from abc import ABC, abstractmethod
from dependency.core import Component, component

class Factory(ABC):
    @abstractmethod
    def work(self):
        pass

@component(
    interface=Factory
)
class FactoryMixin(Component):
    pass