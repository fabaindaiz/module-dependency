from typing import Any
from dependency.core import Provider, provider
from example.module.manager import Manager, ManagerComponent
from example.module.services.factory import Factory, FactoryComponent
from example.module.services.singleton import Singleton, SingletonComponent

@provider(
    component=ManagerComponent,
    imports=[FactoryComponent, SingletonComponent]
)
class Type1Manager(Manager, Provider):
    def __init__(self, cfg: dict[str, Any]):
        print("Manager load")
        self.factory: Factory = FactoryComponent.provide()
        self.singleton: Singleton = SingletonComponent.provide()
    
    def work(self) -> None:
        print("Manager work")
        self.factory.work()
        self.singleton.work()