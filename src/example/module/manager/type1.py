from typing import Any
from dependency.core import Provider, provider
from example.module.manager import Manager, ManagerMixin
from example.module.services.factory import Factory, FactoryMixin
from example.module.services.singleton import Singleton, SingletonMixin

@provider(
    component=ManagerMixin,
    imports=[FactoryMixin, SingletonMixin]
)
class Type1Manager(Provider, Manager):
    def __init__(self, cfg: dict[str, Any]):
        print("Manager load")
        self.factory: Factory = FactoryMixin.provide()
        self.singleton: Singleton = SingletonMixin.provide()
    
    def work(self) -> None:
        print("Manager work")
        self.factory.work()
        self.singleton.work()