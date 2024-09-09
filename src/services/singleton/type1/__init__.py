from pydantic import BaseModel
from typing_extensions import TypedDict
from src.services.singleton import SingletonService

class SingletonConfig(TypedDict):
    key1: str
    key2: str

class Type1SingletonServiceConfig(BaseModel):
    singleton: SingletonConfig

class Type1SingletonService(SingletonService):
    def __init__(self, cfg: dict, **kwargs):
        super().__init__(**kwargs)
        self.__cfg = self.get_config(cfg)
        print(f"Singleton Service init: {self.__cfg.model_dump()}")
    
    @staticmethod
    def get_config(cfg: dict) -> Type1SingletonServiceConfig:
        return Type1SingletonServiceConfig(**cfg)

    def work(self):
        print("Singleton Service work")