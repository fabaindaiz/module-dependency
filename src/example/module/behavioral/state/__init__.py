from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def doThis(self) -> None:
        pass

    @abstractmethod
    def doThat(self) -> None:
        pass