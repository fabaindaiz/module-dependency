from core import provider
from plugin.client import Client
from plugin.manager import Manager

@provider(
    component=Client,
    imports=[Manager]
)
class Type1Client:
    def __init__(self, cfg: dict):
        self.manager = Manager()
        self.manager.work()
        print("Client load")