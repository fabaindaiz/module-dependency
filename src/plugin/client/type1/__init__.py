from src.plugin.client import Client
from src.services.factory.container import FactoryServiceMixin
from src.services.singleton.container import SingletonServiceMixin

class Type1Client(Client, FactoryServiceMixin, SingletonServiceMixin):
    def __init__(self, cfg: dict, **kwargs):
        super().__init__(**kwargs)
        print(f"Client init: {cfg}")

        print("Client load")

    