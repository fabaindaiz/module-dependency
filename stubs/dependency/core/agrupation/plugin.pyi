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
    def on_declaration(cls) -> None:
        """Mark this plugin as a root container in the injection tree.

        Called by ContainerMixin.init_injection when the @module decorator is
        applied. Sets is_root=True on the ContainerInjection so the Registry
        and FallbackPlugin do not treat it as an orphan.
        """
    @classmethod
    def on_resolution(cls, container: Container) -> None:
        """Resolve plugin configuration against the application container.

        Called by ContainerMixin.inject_container when the plugin is attached to
        the application container during module resolution. Delegates to
        resolve_container to validate and populate the config attribute.

        Args:
            container (Container): The application container.
        """
    @classmethod
    def resolve_container(cls, container: Container) -> None:
        """Resolve the plugin configuration.

        Args:
            container (Container): The application container.

        Raises:
            ResolutionError: If the configuration is invalid.
        """
