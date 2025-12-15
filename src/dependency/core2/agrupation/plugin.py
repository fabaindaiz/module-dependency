import logging
from pydantic import BaseModel
from typing import get_type_hints
from dependency.core2.agrupation.module import Module
from dependency.core2.injection.injectable import Injectable
from dependency.core2.exceptions import ResolutionError
from dependency.core2.resolution.container import Container
logger = logging.getLogger("DependencyLoader")

class PluginConfig(BaseModel):
    """Empty configuration model for the plugin.
    """
    pass

class PluginMeta(BaseModel):
    """Metadata for the plugin.
    """
    name: str
    version: str

    def __str__(self) -> str:
        return f"Plugin {self.name} {self.version}"

class Plugin(Module):
    """Plugin class for creating reusable components.
    """
    meta: PluginMeta
    config: BaseModel

    def __resolve_config(self, container: Container) -> None:
        """Resolve the plugin configuration.

        Args:
            config (dict): The configuration dictionary.

        Raises:
            ResolutionError: If the configuration is invalid.
        """
        try:
            config_cls = get_type_hints(self.__class__).get("config", BaseModel)
            config_cls = PluginConfig if config_cls is BaseModel else config_cls
            self.config = config_cls(**container.config())
        except Exception as e:
            raise ResolutionError(f"Failed to resolve plugin config for {self.meta}") from e

    def resolve_providers(self, container: Container) -> list[Injectable]:
        """Resolve provider injections for the plugin.

        Args:
            container (Container): The dependency injection container.

        Returns:
            list[Implementation]: A list of resolved provider injections.
        """
        self.__resolve_config(container=container)
        setattr(container, self.injection.name, self.injection.inject_cls())
        return [provider for provider in self.injection.resolve_providers()]

    def __repr__(self) -> str:
        return f"{self.meta}: {self.config}"
