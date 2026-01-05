from dependency.core.agrupation.module import Module as Module
from dependency.core.exceptions import ResolutionError as ResolutionError
from dependency.core.resolution.container import Container as Container
from pydantic import BaseModel

class PluginConfig(BaseModel):
    """Empty configuration model for the plugin.
    """

class PluginMeta(BaseModel):
    """Metadata for the plugin.
    """
    name: str
    version: str

class Plugin(Module):
    """Plugin class for creating reusable components.
    """
    meta: PluginMeta
    config: BaseModel
    @classmethod
    def resolve_container(cls, container: Container) -> None:
        """Resolve the plugin configuration.

        Args:
            container (Container): The application container.

        Raises:
            ResolutionError: If the configuration is invalid.
        """
