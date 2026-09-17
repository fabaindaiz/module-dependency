from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Reading:
    """One measurement from one sensor.

    Frozen on purpose: a reading is a fact about a moment. Nothing downstream — the
    store, the telemetry observer, the panel — has any business editing it, and making
    that impossible is cheaper than trusting everyone not to.
    """

    sensor: str
    value: float
    taken_at: float

    def __str__(self) -> str:
        return f"{self.sensor}={self.value:.1f}"


class SensorReader(ABC):
    """What every probe can do.

    A plain ABC, not a component: a component has exactly one implementation, and a
    station has several sensors. Each probe declares its own component from this
    interface, which is what lets them be resolved, replaced and grouped individually.
    """

    @property
    @abstractmethod
    def channel(self) -> str:
        """The measurement this probe produces, e.g. 'temperature'."""

    @abstractmethod
    def read(self) -> Reading:
        """Take one measurement now."""
