import logging
from dependency.core import CancelInitialization, instance, providers
from dependency.library.components import CompositeMixin
from example.plugin.runtime.modes import StationMode
from example.plugin.runtime.state import StationState
from example.plugin.sensors.group import SensorGroup
from example.plugin.sensors.interfaces import Reading, SensorReader
from example.plugin.sensors.probes.humidity import HumiditySensor
from example.plugin.sensors.probes.pressure import PressureSensor
from example.plugin.sensors.probes.temperature import TemperatureSensor

_logger = logging.getLogger("station.sensors")

CANDIDATES = (TemperatureSensor, HumiditySensor, PressureSensor)

@instance(
    imports=[
        StationState,
        TemperatureSensor,
        HumiditySensor,
        PressureSensor,
    ],
    provider=providers.Singleton,
)
class FittedSensors(CompositeMixin[SensorReader], SensorGroup):
    """The probes that actually came up on this unit.

    Every candidate is declared as a required import — the station will not start if
    one is missing from the build entirely. Being *declared* and being *fitted* are
    different things though, so each is provided inside a try: a probe that cancelled
    its own initialisation is simply left out, and the station reports DEGRADED rather
    than refusing to run. That distinction is the whole reason CancelInitialization
    exists.
    """
    def __init__(self) -> None:
        super().__init__()
        self.__state: StationState = StationState.provide()

        for candidate in CANDIDATES:
            try:
                self.add(candidate.provide())
            except CancelInitialization as e:
                _logger.warning("probe %s not fitted: %s", candidate.__name__, e)

        if len(self.children) < len(CANDIDATES):
            self.__state.transition(StationMode.DEGRADED)

    def read_all(self) -> list[Reading]:
        return [probe.read() for probe in self.children]
