from dependency.core import Plugin, PluginMeta, module
from example.plugin.storage.settings import StorageConfig


@module()
class StoragePlugin(Plugin):
    """Keeps readings. Which backend is active is decided by imports.py."""

    meta = PluginMeta(name="StoragePlugin", version="1.0.0")
    config: StorageConfig
