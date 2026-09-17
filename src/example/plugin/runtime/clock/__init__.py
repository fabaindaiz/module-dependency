from abc import abstractmethod
from dependency.core import Component, component
from example.plugin.runtime import RuntimePlugin


@component(
    module=RuntimePlugin,
)
class Clock(Component):
    """Time, as a dependency.

    Injecting the clock rather than calling time.time() directly is what lets a test
    drive the station through a hundred samples without waiting for them.
    """

    @abstractmethod
    def now(self) -> float:
        """Seconds since the epoch."""

    @abstractmethod
    def sleep(self, seconds: float) -> None:
        """Block for the given duration."""
