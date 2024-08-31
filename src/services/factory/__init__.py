from abc import ABC, abstractmethod

class FactoryService(ABC):
    @abstractmethod
    def work(self):
        pass