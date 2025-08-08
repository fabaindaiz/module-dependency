from abc import abstractmethod
from pprint import pformat
from pydantic import BaseModel
from dependency_injector import containers, providers
from dependency.core.agrupation.module import Module, module
from dependency.core.injection.container import Container

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

    @property
    @abstractmethod
    def config(self) -> PluginConfig:
        pass

    def set_container(self, container: Container) -> None:
        self.container = container
        setattr(container, self.injection.name, self.injection.inject_cls())

    def __repr__(self):
        return f"{self.meta}: {self.config}"