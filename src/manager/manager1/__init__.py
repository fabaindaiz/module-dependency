from abc import ABC, abstractmethod

class Manager1(ABC):
    @abstractmethod
    def work(self):
        pass