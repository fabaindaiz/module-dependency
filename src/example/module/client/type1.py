from dependency.core import provider
from example.module.client import Client, ClientMixin
from example.module.manager import Manager, ManagerMixin

@provider(
    component=ClientMixin,
    imports=[ManagerMixin]
)
class Type1Client(Client):
    def __init__(self, cfg: dict):
        print("Client load")
        self.manager: Manager = ManagerMixin.provide()
        self.manager.work()