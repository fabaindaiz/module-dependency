from pprint import pformat
from collections import deque
from dependency_injector import containers, providers
from dependency.core.agrupation.module import Module
from dependency.core.injection.container import Container
from pydantic import BaseModel, Field
from typing import TypeVar

C = TypeVar('C', bound='PluginConfig')

class PluginConfig(BaseModel):
    def __str__(self):
        return pformat(self.model_dump())

class PluginMeta(BaseModel):
    name: str
    version: str

    def __str__(self) -> str:
        return f"Plugin {self.name} {self.version}"

class PluginContainer(containers.DynamicContainer):
    config = providers.Configuration()

class Plugin(Module):
    meta: PluginMeta
    container: Container

    def inject(self, container: Container) -> None:
        self.container = container
        setattr(container, self.injection.name, self.injection.inject_cls())
        deque(self.injection.child_inject(), maxlen=0)

    def __repr__(self):
        return f"{self.meta}"