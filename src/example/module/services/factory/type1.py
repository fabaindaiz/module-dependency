from typing import Any
from dependency_injector import providers
from dependency.core import Provider, provider
from example.module.services.settings import Config
from example.module.services.factory import Factory, FactoryMixin

@provider(
    provider=providers.Factory,
    component=FactoryMixin
)
class Type1Factory(Provider, Factory):
    def __init__(self, cfg: dict[str, Any]):
        self.__cfg = Config(**cfg)
        print(f"Factory init")

    def work(self) -> None:
        print("Factory work")