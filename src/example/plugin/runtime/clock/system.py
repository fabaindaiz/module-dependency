import time
from dependency.core import instance, providers
from example.plugin.runtime.clock import Clock

@instance(
    provider=providers.Singleton,
)
class SystemClock(Clock):
    """The real clock. Swap it in an alternative imports.py to run a test fast."""
    def now(self) -> float:
        return time.time()

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)
