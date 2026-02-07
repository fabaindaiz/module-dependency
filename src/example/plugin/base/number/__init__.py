from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugin.base import BasePlugin

@component(
    module=BasePlugin,
)
class NumberService(ABC, Component):
    @abstractmethod
    def getRandomNumber(self) -> int:
        pass
