from pydantic import BaseModel
from dependency_injector import providers
from dependency.core import provider
from example.services.factory import Factory

class FactoryConfig(BaseModel):
    key1: str
    key2: str

class Type1FactoryConfig(BaseModel):
    factory: FactoryConfig

@provider(
    component=Factory,
    provider=providers.Factory
)
class Type1Factory:
    def __init__(self, cfg: dict):
        self.__cfg = self.get_config(cfg)
        print(f"Factory init: {self.__cfg.model_dump()}")
    
    @staticmethod
    def get_config(cfg: dict) -> Type1FactoryConfig:
        return Type1FactoryConfig(**cfg)

    def work(self):
        print("Factory work")