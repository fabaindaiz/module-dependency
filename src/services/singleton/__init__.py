from abc import ABC, abstractmethod
from core import component
from services.singleton.type1 import Type1Singleton

@component(
    selector={
        "type1": Type1Singleton
    }
)
class Singleton(ABC):
    @abstractmethod
    def work(self):
        pass