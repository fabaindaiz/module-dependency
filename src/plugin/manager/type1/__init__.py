from core import provider
from services.factory import Factory
from services.singleton import Singleton

@provider(
    imports=[Factory, Singleton]
)
class Type1Manager:
    def __init__(self, cfg: dict):
        self.factory = Factory()
        self.singleton = Singleton()
        print("Manager load")
    
    def work(self):
        print("Manager work")
        self.factory.work()
        self.factory.work()
        self.singleton.work()
        self.singleton.work()