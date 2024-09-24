from dependency.core import provider
from example.plugin.manager import Manager
from example.services.factory import Factory
from example.services.singleton import Singleton

@provider(
    component=Manager,
    imports=[Factory, Singleton]
)
class Type1Manager(Manager):
    def __init__(self, cfg: dict):
        self.factory = Factory.provided()
        self.singleton = Singleton.provided()
        print("Manager load")
    
    def work(self):
        print("Manager work")
        self.factory.work()
        self.singleton.work()