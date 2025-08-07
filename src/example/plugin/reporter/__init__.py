from dependency.core.agrupation.plugin import Plugin, PluginMeta, module

@module()
class ReporterPlugin(Plugin):
    def declare_providers(self):
        meta = PluginMeta(name="ReporterPlugin", version="0.1.0")