from abc import ABC, abstractmethod
from dependency.core import Component, component

@component()
class Abstraction(Component):
    @abstractmethod
    def feature1(self) -> None:
        pass

    @abstractmethod
    def feature2(self) -> None:
        pass
