from abc import ABC, abstractmethod
from dependency.core import Component, component

class StringService(ABC):
    @abstractmethod
    def getRandomString(self) -> str:
        pass

@component(
    interface=StringService
)
class StringServiceComponent(Component):
    pass