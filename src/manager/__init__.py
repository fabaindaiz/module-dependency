from abc import ABC, abstractmethod
from core import module

@module(
)
class Manager(ABC):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def work(self):
        pass