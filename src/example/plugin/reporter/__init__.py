from dependency.core import Plugin, PluginMeta, module

@module()
class ReporterPlugin(Plugin):
    meta = PluginMeta(name="ReporterPlugin", version="0.1.0")