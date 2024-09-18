from core import provider
from pydantic import BaseModel
from services.singleton import Singleton

class SingletonConfig(BaseModel):
    key1: str
    key2: str

class Type1SingletonConfig(BaseModel):
    singleton: SingletonConfig

@provider(
    component=Singleton
)
class Type1Singleton:
    def __init__(self, cfg: dict):
        self.__cfg = self.get_config(cfg)
        print(f"Singleton init: {self.__cfg.model_dump()}")
    
    @staticmethod
    def get_config(cfg: dict) -> Type1SingletonConfig:
        return Type1SingletonConfig(**cfg)

    def work(self):
        print("Singleton work")