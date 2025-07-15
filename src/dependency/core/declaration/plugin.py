from abc import ABC, abstractmethod
from pprint import pformat
from pydantic import BaseModel, Field

class PluginConfig(BaseModel):
    def __str__(self):
        return pformat(self.model_dump())

class PluginMeta(BaseModel):
    name: str
    version: str

    def __str__(self) -> str:
        return f"Plugin {self.name} {self.version}"

class Plugin(ABC):
    config_cls: type[PluginConfig]
    meta: PluginMeta

    def __init__(self,
            config: dict,
            ) -> None:
        self._config = self.config_cls(**config)
    
    def __repr__(self):
        return f"{self.meta} with config:\n{self._config}"