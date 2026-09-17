from collections import deque
from dependency.core import instance, providers
from example.plugin.sensors.interfaces import Reading
from example.plugin.storage import StoragePlugin
from example.plugin.storage.store import ReadingStore


@instance(
    provider=providers.Singleton,
)
class InMemoryStore(ReadingStore):
    """Bounded ring buffer. The default: an embedded unit should not fill its flash
    by default, and a station that has been up for a month does not need every sample."""

    def __init__(self) -> None:
        self.__readings: deque[Reading] = deque(
            maxlen=StoragePlugin.config.storage.keep_last
        )

    def append(self, reading: Reading) -> None:
        self.__readings.append(reading)

    def recent(self, limit: int = 10) -> list[Reading]:
        return list(self.__readings)[-limit:]
