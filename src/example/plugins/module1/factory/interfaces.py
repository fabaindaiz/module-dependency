from abc import ABC, abstractmethod

class Product(ABC):
    @abstractmethod
    def doStuff(self, operation: str) -> None:
        pass