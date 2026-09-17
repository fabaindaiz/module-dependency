from abc import abstractmethod
from dependency.core import Component, component
from example.plugin.sensors.interfaces import Reading
from example.plugin.storage import StoragePlugin

@component(
    module=StoragePlugin,
)
class ReadingStore(Component):
    """Where readings go.

    The sampler depends on this interface and not on a file, which is what lets the
    same station run against memory in a test and against the disk on the unit.
    """
    @abstractmethod
    def append(self, reading: Reading) -> None:
        """Record one reading."""

    @abstractmethod
    def recent(self, limit: int = 10) -> list[Reading]:
        """The most recent readings, newest last."""
