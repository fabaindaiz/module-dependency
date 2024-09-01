from abc import ABC, abstractmethod

class Manager(ABC):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def work(self):
        pass