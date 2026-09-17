import math
from dependency.core import Component, component, instance, providers
from example.plugin.runtime.clock import Clock
from example.plugin.sensors import SensorsPlugin
from example.plugin.sensors.interfaces import Reading, SensorReader


@component(
    module=SensorsPlugin,
)
class TemperatureSensor(SensorReader, Component):
    """The temperature probe. One component, so one active implementation."""


@instance(
    imports=[Clock],
    provider=providers.Singleton,
)
class SimulatedTemperature(TemperatureSensor):
    """Stands in for hardware: a slow sine that crosses the alert threshold."""

    def __init__(self) -> None:
        self.__clock: Clock = Clock.provide()

    @property
    def channel(self) -> str:
        return "temperature"

    def read(self) -> Reading:
        now = self.__clock.now()
        value = 55.0 + 12.0 * math.sin(now)
        return Reading(sensor=self.channel, value=value, taken_at=now)
