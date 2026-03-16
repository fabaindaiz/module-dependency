from dependency.core import Plugin
from example.plugin.base import BasePlugin
from example.plugin.hardware import HardwarePlugin
from example.plugin.reporter import ReporterPlugin

PLUGINS: list[type[Plugin]] = [
    BasePlugin,
    HardwarePlugin,
    ReporterPlugin
]
