from typing import Any
from dependency_injector import providers
from dependency.core import Provider, provider
from example.module.services.settings import Config
from example.module.services.factory import Factory, FactoryComponent

@provider(
    provider=providers.Factory,
    component=FactoryComponent
)
class Type1Factory(Factory, Provider):
    def __init__(self, cfg: dict[str, Any]):
        self.__cfg = Config(**cfg)
        print(f"Factory init")

    def work(self) -> None:
        print("Factory work")