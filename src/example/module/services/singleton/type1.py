from typing import Any
from dependency.core import Provider, provider
from example.module.services.settings import Config
from example.module.services.singleton import Singleton, SingletonMixin

@provider(
    component=SingletonMixin
)
class Type1Singleton(Provider, Singleton):
    def __init__(self, cfg: dict[str, Any]):
        self.__cfg = Config(**cfg)
        print(f"Singleton init")

    def work(self) -> None:
        print("Singleton work")