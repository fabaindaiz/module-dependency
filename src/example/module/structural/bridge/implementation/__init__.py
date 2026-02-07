from abc import ABC, abstractmethod
from dependency.core import Component, component

@component()
class Implementation(ABC, Component):
    @abstractmethod
    def method1(self):
        pass

    @abstractmethod
    def method2(self):
        pass

    @abstractmethod
    def method3(self):
        pass
