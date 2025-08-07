from dependency.core import Plugin, PluginMeta, module

@module()
class HardwarePlugin(Plugin):
    meta = PluginMeta(name="HardwarePlugin", version="0.1.0")