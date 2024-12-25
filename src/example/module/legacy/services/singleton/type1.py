from typing import Any
from dependency.core import provider
from example.module.services.settings import Config
from example.module.services.singleton import Singleton, SingletonComponent

@provider(
    component=SingletonComponent
)
class Type1Singleton(Singleton):
    def __init__(self, cfg: dict[str, Any]):
        self.__cfg = Config(**cfg)
        print(f"Singleton init")

    def work(self) -> None:
        print("Singleton work")