from dependency.core import Plugin, PluginMeta, module
from example.plugin.runtime.settings import RuntimeConfig


@module()
class RuntimePlugin(Plugin):
    """Process-level services: the clock, the async loop, and the station's state.

    Everything else depends on this plugin, and it depends on nothing.
    """

    meta = PluginMeta(name="RuntimePlugin", version="1.0.0")
    config: RuntimeConfig
