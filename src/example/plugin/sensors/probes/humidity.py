from dependency.core import Component, component, instance, providers
from example.plugin.runtime.clock import Clock
from example.plugin.sensors import SensorsPlugin
from example.plugin.sensors.interfaces import Reading, SensorReader


@component(
    module=SensorsPlugin,
)
class HumiditySensor(SensorReader, Component):
    """The humidity probe."""


@instance(
    imports=[Clock],
    provider=providers.Singleton,
)
class SimulatedHumidity(HumiditySensor):
    """A slow ramp that stays inside its threshold, so the alert path can be seen
    firing for one channel and not the other."""

    def __init__(self) -> None:
        self.__clock: Clock = Clock.provide()
        self.__samples: int = 0

    @property
    def channel(self) -> str:
        return "humidity"

    def read(self) -> Reading:
        self.__samples += 1
        value = 40.0 + (self.__samples % 10)
        return Reading(sensor=self.channel, value=value, taken_at=self.__clock.now())
