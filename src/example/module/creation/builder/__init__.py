from abc import ABC, abstractmethod
from dependency.core import Component, component

class BuilderInterface(ABC):
    @abstractmethod
    def stepA(self) -> None:
        pass

    @abstractmethod
    def stepB(self) -> None:
        pass

    @abstractmethod
    def work(self) -> None:
        pass

class Builder(ABC):
    def reset(self) -> None:
        pass

    @abstractmethod
    def buildStepA(self) -> None:
        pass
    
    @abstractmethod
    def buildStepB(self) -> None:
        pass

    @abstractmethod
    def result(self) -> BuilderInterface:
        pass

@component(
    interface=Builder
)
class BuilderComponent(Component):
    pass