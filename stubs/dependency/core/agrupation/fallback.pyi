from dependency.core.agrupation.module import module as module
from dependency.core.agrupation.plugin import Plugin as Plugin, PluginMeta as PluginMeta
from dependency.core.resolution.registry import Registry as Registry
from dependency_injector import containers as containers

def initialize_fallback(parent: containers.Container) -> type[Plugin]: ...
