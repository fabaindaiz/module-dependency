
from dependency.core.declaration import Plugin, PluginMeta
from .settings import BasePluginConfig


class BasePlugin(Plugin):
    config_cls = BasePluginConfig
    meta = PluginMeta(
        name="BasePlugin",
        version="v1.0.0")

    @property
    def config(self) -> BasePluginConfig:
        return self._config

if __name__ == "__main__":
    config = {"general": {"debug": True}}
    plugin = BasePlugin(config=config)
    print(plugin)