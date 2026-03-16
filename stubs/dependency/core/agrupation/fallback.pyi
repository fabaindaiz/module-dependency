from _typeshed import Incomplete
from dependency.core.agrupation.module import module as module
from dependency.core.agrupation.plugin import Plugin as Plugin, PluginMeta as PluginMeta
from dependency.core.resolution.registry import Registry as Registry
from dependency_injector import containers as containers

class FallbackInternal(Plugin):
    meta: Incomplete
    @classmethod
    def initialize_fallback(cls, parent: containers.Container) -> None: ...
