from abc import ABC, abstractmethod

class Service1(ABC):
    @abstractmethod
    def init(self, cfg: dict):
        pass
    
    @abstractmethod
    def work(self):
        pass