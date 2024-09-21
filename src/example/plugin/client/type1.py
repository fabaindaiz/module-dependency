from dependency.core import provider
from example.plugin.client import Client
from example.plugin.manager import Manager

@provider(
    component=Client,
    imports=[Manager]
)
class Type1Client:
    def __init__(self, cfg: dict):
        self.manager = Manager.provided()
        self.manager.work()
        print("Client load")