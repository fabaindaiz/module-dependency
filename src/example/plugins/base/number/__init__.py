from abc import ABC, abstractmethod
from dependency.core import Component, component

class NumberService(ABC):
    @abstractmethod
    def getRandomNumber(self) -> int:
        pass

@component(
    interface=NumberService
)
class NumberServiceComponent(Component):
    pass