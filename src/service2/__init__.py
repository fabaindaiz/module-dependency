from abc import ABC, abstractmethod

class Service2(ABC):
    @abstractmethod
    def init(self, cfg: dict):
        pass

    @abstractmethod
    def work(self):
        pass