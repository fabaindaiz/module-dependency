from dependency.core import provider
from example.plugin.manager import Manager, ManagerMixin
from example.services.factory import Factory, FactoryMixin
from example.services.singleton import Singleton, SingletonMixin

@provider(
    component=ManagerMixin,
    imports=[FactoryMixin, SingletonMixin]
)
class Type1Manager(Manager):
    def __init__(self, cfg: dict):
        print("Manager load")
        self.factory: Factory = FactoryMixin.provide()
        self.singleton: Singleton = SingletonMixin.provide()
    
    def work(self):
        print("Manager work")
        self.factory.work()
        self.singleton.work()