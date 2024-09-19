from core import provider
from plugin.manager import Manager

@provider(
    imports=[Manager]
)
class Type1Client:
    def __init__(self, cfg: dict):
        self.manager = Manager()
        self.manager.work()
        print("Client load")