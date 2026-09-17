import json
from collections import deque
from pathlib import Path
from typing import Iterator, TextIO
from dependency.core import instance, providers
from example.plugin.sensors.interfaces import Reading
from example.plugin.storage import StoragePlugin
from example.plugin.storage.store import ReadingStore

@instance(
    provider=providers.Resource,
)
class JsonlStore(ReadingStore):
    """Appends every reading to a file, one JSON object per line.

    providers.Resource rather than Singleton because this one owns a file handle.
    Resource is the provider with a lifecycle: __enter__ opens, __exit__ closes.

    Measured caveat, and the reason MonitoringStation.stop() exists: the root
    Container does not see providers that live inside plugin sub-containers — its
    own .providers is just ['__self__'] — so container.shutdown_resources() is a
    no-op here and initialisation is lazy, on first .provide(). The application has
    to shut its own resources down. See D-034.

    Import this module instead of store.memory to switch the station to disk.
    """
    def __init__(self) -> None:
        self.__path = Path(StoragePlugin.config.storage.path)
        self.__path.parent.mkdir(parents=True, exist_ok=True)
        self.__handle: TextIO = self.__path.open("a", encoding="utf-8")
        self.__recent: deque[Reading] = deque(
            maxlen=StoragePlugin.config.storage.keep_last)

    def append(self, reading: Reading) -> None:
        self.__handle.write(json.dumps({
            "sensor": reading.sensor,
            "value": reading.value,
            "taken_at": reading.taken_at,
        }) + "\n")
        self.__handle.flush()
        self.__recent.append(reading)

    def recent(self, limit: int = 10) -> list[Reading]:
        return list(self.__recent)[-limit:]

    def __enter__(self) -> "JsonlStore":
        return self

    def __exit__(self, *exc: object) -> None:
        """Closes the handle. Driven by MonitoringStation.stop()."""
        self.__handle.close()
