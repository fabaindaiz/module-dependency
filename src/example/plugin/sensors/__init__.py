from dependency.core import Plugin, PluginMeta, module
from example.plugin.sensors.settings import SensorsConfig

@module()
class SensorsPlugin(Plugin):
    """Reads the hardware and turns it into Readings on a fixed cadence."""
    meta = PluginMeta(name="SensorsPlugin", version="1.0.0")
    config: SensorsConfig
