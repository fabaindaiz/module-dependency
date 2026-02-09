from abc import ABC, abstractmethod
from dependency.core import Component, component


@component()
class Abstraction(ABC, Component):
    @abstractmethod
    def feature1(self):
        pass

    @abstractmethod
    def feature2(self):
        pass
