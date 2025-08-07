from dependency.core import Plugin, PluginMeta, module

@module()
class BasePlugin(Plugin):
    meta = PluginMeta(name="BasePlugin", version="0.1.0")