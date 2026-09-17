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
        """Mark this plugin as a root container in the injection tree."""
        cls.injection.is_root = True

    @classmethod
    def on_resolution(cls, container: Container) -> None:
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
            hints = get_type_hints(cls)
            if "config" not in hints:
                # A plugin that needs no configuration is ordinary. Warning about it made
                # the first thing a new user saw a complaint about nothing (D-054).
                _logger.debug(f"Plugin {cls.meta} declares no configuration")
                return
            config_cls = hints["config"]
            if issubclass(config_cls, BaseModel):
                # noqa B010: `config` is declared as a type hint on the subclass and does
                # not exist on Plugin, so plain assignment does not type-check.
                setattr(cls, "config", config_cls.model_validate(container.config()))  # noqa: B010
            else:
                _logger.warning(
                    f"Plugin {cls.meta} declares config: {config_cls!r}, which is not a "
                    f"BaseModel — it will never be populated"
                )
        except ValidationError as e:
            raise ProvisionError(
                f"Plugin {cls.meta} configuration validation failed"
            ) from e
