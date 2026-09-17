from dependency.core import Plugin, PluginMeta, module
from example.plugin.telemetry.settings import TelemetryConfig

@module()
class TelemetryPlugin(Plugin):
    """Turns readings into events, and events into alerts."""
    meta = PluginMeta(name="TelemetryPlugin", version="1.0.0")
    config: TelemetryConfig
