import logging
from pydantic import BaseModel, ValidationError
from typing import get_type_hints
from dependency.core.agrupation.module import Module
from dependency.core.resolution.container import Container
from dependency.core.exceptions import ProvisionError
_logger = logging.getLogger("dependency.loader")

class PluginMeta(BaseModel):
    """Metadata for the plugin.

    Attributes:
        name (str): Name of the plugin
        version (str): Version of the plugin
    """
    name: str
    version: str

    def __str__(self) -> str:
        return f"Plugin {self.name} ({self.version})"

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
        cls.injection.is_root = True

    @classmethod
    def on_resolution(cls,
        container: Container
    ) -> None:
        """Resolve plugin configuration against the application container.

        Called by ContainerMixin.inject_container when the plugin is attached to
        the application container during module resolution. Delegates to
        resolve_container to validate and populate the config attribute.

        Args:
            container (Container): The application container.
        """
        cls.resolve_container(container=container)

    @classmethod
    def resolve_container(cls, container: Container) -> None:
        """Resolve the plugin configuration.

        Args:
            container (Container): The application container.

        Raises:
            ResolutionError: If the configuration is invalid.
        """
        try:
            config_cls = get_type_hints(cls).get("config", object)
            if issubclass(config_cls, BaseModel):
                setattr(cls, "config", config_cls.model_validate(container.config()))
            else:
                _logger.warning(f"Plugin {cls.meta} configuration class is not a subclass of BaseModel")
        except ValidationError as e:
            raise ProvisionError(f"Plugin {cls.meta} configuration validation failed") from e
