from abc import ABC, abstractmethod
from core import component

@component(
    
)
class Singleton(ABC):
    @abstractmethod
    def work(self):
        pass