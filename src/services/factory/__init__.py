from abc import ABC, abstractmethod
from core import component
from services.factory.type1 import Type1Factory

@component(
    selector={
        "type1": Type1Factory
    }
)
class Factory(ABC):
    @abstractmethod
    def work(self):
        pass