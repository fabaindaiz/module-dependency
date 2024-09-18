from abc import ABC, abstractmethod

class Manager(ABC):
    @abstractmethod
    def work(self):
        pass