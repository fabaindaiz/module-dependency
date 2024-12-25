from abc import ABC, abstractmethod
from dependency.core import Component, component

class AbtractFactoryInterface1(ABC):
    @abstractmethod
    def work1(self) -> None:
        pass

class AbtractFactoryInterface2(ABC):
    @abstractmethod
    def work2(self) -> None:
        pass

class AbtractFactory(ABC):
    def work(self) -> None:
        instance1 = self.createType1()
        instance2 = self.createType2()
        instance1.work1()
        instance2.work2()

    @abstractmethod
    def createType1(self) -> AbtractFactoryInterface1:
        pass

    @abstractmethod
    def createType2(self) -> AbtractFactoryInterface2:
        pass

@component(
    interface=AbtractFactory
)
class AbtractFactoryComponent(Component):
    pass