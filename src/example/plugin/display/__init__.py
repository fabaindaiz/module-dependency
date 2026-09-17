from pydantic import BaseModel
from dependency.core import Plugin, PluginMeta, module


class DisplaySettings(BaseModel):
    width: int = 40


class DisplayConfig(BaseModel):
    display: DisplaySettings = DisplaySettings()


@module()
class DisplayPlugin(Plugin):
    """An optional front panel.

    This plugin is the point of the example: a unit that ships without a screen leaves
    it out of PLUGINS, and nothing else changes. Telemetry declares StatusPanel as an
    OPTIONAL import, so it resolves either way.
    """
    meta = PluginMeta(name="DisplayPlugin", version="1.0.0")
    config: DisplayConfig
