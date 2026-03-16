import logging
from dependency_injector import containers
from dependency.core.agrupation.module import module
from dependency.core.agrupation.plugin import Plugin, PluginMeta
from dependency.core.resolution.registry import Registry
_logger = logging.getLogger("dependency.loader")

def initialize_fallback(parent: containers.Container) -> type[Plugin]:
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
