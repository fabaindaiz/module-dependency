from dependency.core import provider
from example.plugin.client import Client, ClientMixin
from example.plugin.manager import Manager, ManagerMixin

@provider(
    component=ClientMixin,
    imports=[ManagerMixin]
)
class Type1Client(Client):
    def __init__(self, cfg: dict):
        print("Client load")
        self.manager: Manager = ManagerMixin.provide()
        self.manager.work()