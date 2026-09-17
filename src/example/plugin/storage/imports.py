# Swap this line for store.jsonl to persist readings to disk. Nothing else changes:
# the sampler depends on the ReadingStore interface, not on a backend.
import example.plugin.storage.store.memory

from example.plugin.storage import StoragePlugin
__all__ = ["StoragePlugin"]
