from abc import ABC, abstractmethod
from core import module

@module(
)
class Manager(ABC):
    @abstractmethod
    def work(self):
        pass