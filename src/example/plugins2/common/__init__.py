from dependency.core.agrupation.plugin import Plugin, PluginMeta, module
from example.plugins.common.settings import CommonPluginConfig

@module()
class CommonPlugin(Plugin):
    meta = PluginMeta(name="common_plugin", version="0.1.0")
    
    @property
    def config(self) -> CommonPluginConfig:
        return CommonPluginConfig(**self.container.config())