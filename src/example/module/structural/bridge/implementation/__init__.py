from abc import ABC, abstractmethod
from dependency.core import Component, component

@component()
class Implementation(Component):
    @abstractmethod
    def method1(self) -> None:
        pass

    @abstractmethod
    def method2(self) -> None:
        pass

    @abstractmethod
    def method3(self) -> None:
        pass
