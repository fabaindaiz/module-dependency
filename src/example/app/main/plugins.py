from dependency.core import Plugin
from example.plugin.display import DisplayPlugin
from example.plugin.runtime import RuntimePlugin
from example.plugin.sensors import SensorsPlugin
from example.plugin.storage import StoragePlugin
from example.plugin.telemetry import TelemetryPlugin

PLUGINS: list[type[Plugin]] = [
    RuntimePlugin,
    SensorsPlugin,
    StoragePlugin,
    TelemetryPlugin,
    # Remove DisplayPlugin to build a unit without a screen. Nothing else changes:
    # telemetry declares StatusPanel under optional=, so it resolves either way.
    DisplayPlugin,
]
