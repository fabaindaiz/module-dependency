from dependency.core.agrupation.module import Module as Module
from dependency.core.exceptions import ProvisionError as ProvisionError
from dependency.core.resolution.container import Container as Container
from pydantic import BaseModel

class PluginMeta(BaseModel):
    """Metadata for the plugin.

    Attributes:
        name (str): Name of the plugin
        version (str): Version of the plugin
    """
    name: str
    version: str

class Plugin(Module):
    """Plugin class for creating reusable components.

    Attributes:
        meta (PluginMeta): Metadata for the plugin
        config (BaseModel): Configuration model for the plugin
    """
    meta: PluginMeta
    @classmethod
    def on_declaration(cls) -> None: ...
    @classmethod
    def on_resolution(cls, container: Container) -> None: ...
    @classmethod
    def resolve_container(cls, container: Container) -> None:
        """Resolve the plugin configuration.

        Args:
            container (Container): The application container.

        Raises:
            ResolutionError: If the configuration is invalid.
        """
