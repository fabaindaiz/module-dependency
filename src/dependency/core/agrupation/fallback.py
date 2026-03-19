import logging
from dependency_injector import containers
from dependency.core.agrupation.module import module
from dependency.core.agrupation.plugin import Plugin, PluginMeta
from dependency.core.resolution.registry import Registry
_logger = logging.getLogger("dependency.loader")

def initialize_fallback(parent: containers.Container) -> type[Plugin]:
    """Create and initialize the internal FallbackPlugin.

    The FallbackPlugin adopts all orphan providers — providers that were declared
    without a parent module and therefore have no ContainerInjection node in the
    tree. Without adoption, these providers would fail resolution because they
    cannot build a reference string for wiring.

    Orphan providers are attached to the FallbackPlugin's container, marked with
    strict_resolution=False so they do not block resolution if they lack an
    implementation, and their providers are resolved against the parent container.

    This function is called once during Entrypoint.initialize() before the main
    resolution phases run. It is an internal safety mechanism — orphan providers
    should ideally be assigned to a proper module.

    Args:
        parent (containers.Container): The root application container.

    Returns:
        type[Plugin]: The dynamically created FallbackInternal plugin class.
    """
    @module()
    class FallbackInternal(Plugin):
        meta = PluginMeta(name="FallbackPlugin", version="1.0.0")

        @classmethod
        def initialize_fallback(cls, parent: containers.Container) -> None:
            #for container in Registry.containers:
            #    if container.parent is None and not container.is_root:
            #        _logger.debug(f"Container {container} has been registered to fallback module")
            #        container.change_parent(cls.injection)
            for provider in Registry.providers:
                if provider.parent is None and not provider.is_root:
                    _logger.debug(f"Provider {provider} has been registered to fallback module")
                    provider.injectable.strict_resolution = False
                    provider.change_parent(cls.injection)
            cls.resolve_providers(container=parent)

    FallbackInternal.initialize_fallback(parent=parent)
    return FallbackInternal
