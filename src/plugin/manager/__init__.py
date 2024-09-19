from abc import ABC, abstractmethod
from core import component
from plugin.manager.type1 import Type1Manager

@component(
    selector={
        "type1": Type1Manager
    }
)
class Manager(ABC):
    @abstractmethod
    def work(self):
        pass