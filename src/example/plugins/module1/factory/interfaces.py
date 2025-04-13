from abc import ABC, abstractmethod

class Product(ABC):
    @abstractmethod
    def doStuff(self) -> None:
        pass