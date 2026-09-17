from dependency.core import instance, providers
from example.plugin.runtime.clock import Clock

@instance(
    provider=providers.Singleton,
)
class ManualClock(Clock):
    """A clock that never waits.

    Importing this module instead of clock.system is the whole mechanism for making
    the station run at full speed under test: no declaration changes, only which
    module the active imports.py pulls in.
    """
    def __init__(self) -> None:
        self._now: float = 0.0

    def now(self) -> float:
        return self._now

    def sleep(self, seconds: float) -> None:
        self._now += seconds
