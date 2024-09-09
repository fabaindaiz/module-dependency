from pydantic import BaseModel
from src.services.factory import FactoryService

class FactoryConfig(BaseModel):
    key1: str
    key2: str

class Type1FactoryServiceConfig(BaseModel):
    factory: FactoryConfig

class Type1FactoryService(FactoryService):
    def __init__(self, cfg: dict, **kwargs):
        super().__init__(**kwargs)
        self.__cfg = self.get_config(cfg)
        print(f"Factory Service init: {self.__cfg.model_dump()}")
    
    @staticmethod
    def get_config(cfg: dict) -> Type1FactoryServiceConfig:
        return Type1FactoryServiceConfig(**cfg)

    def work(self):
        print("Factory Service work")