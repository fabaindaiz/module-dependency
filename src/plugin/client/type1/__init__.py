from src.plugin.client import Client
from src.plugin.manager.container import ManagerMixin

class Type1Client(Client, ManagerMixin):
    def __init__(self, cfg: dict, **kwargs):
        super().__init__(**kwargs)
        self.manager.work()
        print("Client load")