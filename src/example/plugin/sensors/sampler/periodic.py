import logging
from dependency.core import instance, providers
from example.plugin.runtime.modes import StationMode
from example.plugin.runtime.state import StationState
from example.plugin.sensors import SensorsPlugin
from example.plugin.sensors.group import SensorGroup
from example.plugin.sensors.sampler import Sampler
from example.plugin.sensors.interfaces import Reading
from example.plugin.storage.store import ReadingStore
from example.plugin.telemetry.events import ReadingTaken, ThresholdExceeded
from example.plugin.telemetry.observer import StationObserver

_logger = logging.getLogger("station.sensors")

@instance(
    imports=[
        SensorGroup,
        ReadingStore,
        StationObserver,
        StationState,
    ],
    provider=providers.Singleton,
    bootstrap=True,
)
class PeriodicSampler(Sampler):
    """Samples every fitted probe, stores each reading, and publishes its events.

    bootstrap=True so the sampler is constructed while the station is coming up: if a
    probe or the store is broken, it fails in front of whoever is watching the unit
    start, not an hour later.

    The warm-up is deliberately *not* here. Bootstrap order is unspecified, so
    sampling from __init__ could publish before the alert sink has subscribed. The
    entrypoint calls warmup() once the graph is fully initialised.
    """
    def __init__(self) -> None:
        self.__group: SensorGroup = SensorGroup.provide()
        self.__store: ReadingStore = ReadingStore.provide()
        self.__observer: StationObserver = StationObserver.provide()
        self.__state: StationState = StationState.provide()
        self.__thresholds = SensorsPlugin.config.sensors.thresholds
        _logger.info("sampler ready with %d probe(s)", len(self.__group.children))

    def warmup(self) -> None:
        for _ in range(SensorsPlugin.config.sensors.warmup_samples):
            self.sample_once()
        if self.__state.state is StationMode.STARTING:
            self.__state.transition(StationMode.SAMPLING)

    def sample_once(self) -> list[Reading]:
        readings = self.__group.read_all()
        for reading in readings:
            self.__store.append(reading)
            self.__observer.update(ReadingTaken(reading=reading))

            limit = self.__thresholds.get(reading.sensor)
            if limit is not None and reading.value > limit:
                self.__observer.update(
                    ThresholdExceeded(reading=reading, limit=limit))
        return readings
