from dependency.core.agrupation.module import module as module
from dependency.core.agrupation.plugin import Plugin as Plugin, PluginMeta as PluginMeta
from dependency.core.resolution.registry import Registry as Registry
from dependency_injector import containers as containers

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
