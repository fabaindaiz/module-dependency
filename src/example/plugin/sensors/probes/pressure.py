from dependency.core import CancelInitialization, Component, component, instance, providers
from example.plugin.sensors import SensorsPlugin
from example.plugin.sensors.interfaces import Reading, SensorReader

@component(
    module=SensorsPlugin,
)
class PressureSensor(SensorReader, Component):
    """The pressure probe — the one that is not fitted on every unit."""

@instance(
    provider=providers.Singleton,
    bootstrap=True,
)
class AbsentPressure(PressureSensor):
    """Hardware that is not present on this build.

    bootstrap=True means the station tries to bring it up at startup, and
    CancelInitialization is how it declines without failing the graph: the station
    logs it, carries on, and SensorGroup leaves this channel out. Any other exception
    here would become an InitializationError and stop the station, which is the right
    behaviour for a bug and the wrong one for a missing option.
    """
    def __init__(self) -> None:
        raise CancelInitialization("no pressure probe fitted on this unit")

    @property
    def channel(self) -> str:
        return "pressure"

    def read(self) -> Reading:  # pragma: no cover - never constructed
        raise NotImplementedError
