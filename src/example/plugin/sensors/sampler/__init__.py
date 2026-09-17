from abc import abstractmethod
from dependency.core import Component, component
from example.plugin.sensors import SensorsPlugin
from example.plugin.sensors.interfaces import Reading

@component(
    module=SensorsPlugin,
)
class Sampler(Component):
    """Drives one pass over the sensors and hands the readings on."""
    @abstractmethod
    def warmup(self) -> None:
        """Take the configured warm-up samples.

        Called explicitly by the entrypoint after initialize(), never from __init__.
        Bootstrap order is unspecified — ResolutionStrategy.initialize iterates a set —
        so anything that must happen after every subscriber is registered has to be
        sequenced from the composition root. See D-035.
        """

    @abstractmethod
    def sample_once(self) -> list[Reading]:
        """Take one reading per fitted probe and publish it."""
