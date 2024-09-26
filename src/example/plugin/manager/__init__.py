from abc import ABC, abstractmethod
from dependency.core import Component, component

class Manager(ABC):
    @abstractmethod
    def work(self):
        pass

@component(
    interface=Manager
)
class ManagerMixin(Component):
    pass