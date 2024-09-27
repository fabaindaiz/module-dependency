from typing import Any
from dependency.core import Provider, provider
from example.module.client import Client, ClientMixin
from example.module.manager import Manager, ManagerMixin

@provider(
    component=ClientMixin,
    imports=[ManagerMixin]
)
class Type1Client(Provider, Client):
    def __init__(self, cfg: dict[str, Any]):
        print("Client load")
        self.manager: Manager = ManagerMixin.provide()
        self.manager.work()