from abc import ABC, abstractmethod
from core import component

@component(
    
)
class Factory(ABC):
    @abstractmethod
    def work(self):
        pass