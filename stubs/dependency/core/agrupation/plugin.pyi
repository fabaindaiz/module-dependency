from dependency.core.agrupation.module import Module as Module
from dependency.core.exceptions import DependencyError as DependencyError
from dependency.core.injection.base import ProviderInjection as ProviderInjection
from dependency.core.injection.container import Container as Container
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
    def resolve_providers(self, container: Container) -> list[ProviderInjection]:
        """Resolve provider injections for the plugin.

        Args:
            container (Container): The dependency injection container.

        Returns:
            list[ProviderInjection]: A list of resolved provider injections.
        """
