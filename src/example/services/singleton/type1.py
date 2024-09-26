from dependency.core import provider
from example.services.settings import Config
from example.services.singleton import Singleton, SingletonMixin

@provider(
    component=SingletonMixin
)
class Type1Singleton(Singleton):
    def __init__(self, cfg: dict):
        self.__cfg = Config(**cfg)
        print(f"Singleton init")

    def work(self):
        print("Singleton work")