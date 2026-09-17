from dataclasses import dataclass
from dependency.library.patterns.observer import EventContext
from example.plugin.sensors.interfaces import Reading


class StationEvent(EventContext):
    """Base for everything the station publishes.

    Subscribers are matched on the exact type of the context, so a listener for
    ThresholdExceeded never sees a plain ReadingTaken.
    """


@dataclass
class ReadingTaken(StationEvent):
    reading: Reading


@dataclass
class ThresholdExceeded(StationEvent):
    reading: Reading
    limit: float
