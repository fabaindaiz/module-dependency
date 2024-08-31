from abc import ABC, abstractmethod

class SingletonService(ABC):
    @abstractmethod
    def work(self):
        pass