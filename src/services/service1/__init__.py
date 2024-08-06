from abc import ABC, abstractmethod

class Service1(ABC):
    @abstractmethod
    def work(self):
        pass