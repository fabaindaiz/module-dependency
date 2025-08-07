from abc import ABC, abstractmethod
from dependency.core import Component, component

class Factory(ABC):
    @abstractmethod
    def create(self) -> Component:
        pass