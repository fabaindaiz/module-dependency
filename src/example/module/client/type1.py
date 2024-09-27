from typing import Any
from dependency.core import Provider, provider
from example.module.client import Client, ClientComponent
from example.module.manager import Manager, ManagerComponent

@provider(
    component=ClientComponent,
    imports=[ManagerComponent]
)
class Type1Client(Client, Provider):
    def __init__(self, cfg: dict[str, Any]) -> None:
        print("Client load")
        self.manager: Manager = ManagerComponent.provide()
        self.manager.work()