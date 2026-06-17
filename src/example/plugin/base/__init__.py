from dependency.core import Container, Plugin, PluginMeta, module
from example.plugin.base.settings import BasePluginConfig

@module(
    provides=[

    ]
)
class BasePlugin(Plugin):
    meta = PluginMeta(name="BasePlugin", version="0.1.0")
    config: BasePluginConfig

    @classmethod
    def on_resolution(cls, container: Container):
        super().on_resolution(container)
        print(f"{cls.meta} resolved with config: {cls.config}")
