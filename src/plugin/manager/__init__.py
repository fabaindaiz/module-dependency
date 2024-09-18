from abc import ABC, abstractmethod
from core import component

@component(
)
class Manager(ABC):
    @abstractmethod
    def work(self):
        pass