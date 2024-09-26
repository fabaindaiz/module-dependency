from dependency.core import provider
from dependency_injector import providers
from example.module.services.settings import Config
from example.module.services.factory import Factory, FactoryMixin

@provider(
    provider=providers.Factory,
    component=FactoryMixin
)
class Type1Factory(Factory):
    def __init__(self, cfg: dict):
        self.__cfg = Config(**cfg)
        print(f"Factory init")

    def work(self):
        print("Factory work")