from abc import ABC, abstractmethod

class Service2(ABC):
    @abstractmethod
    def work(self):
        pass