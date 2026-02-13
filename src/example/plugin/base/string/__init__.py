from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugin.base import BasePlugin

@component(
    module=BasePlugin,
)
class StringService(ABC, Component):
    @abstractmethod
    def getRandomString(self) -> str:
        pass
