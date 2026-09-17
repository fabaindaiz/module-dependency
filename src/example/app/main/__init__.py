import asyncio
import logging
from pathlib import Path
from typing import Optional
from dependency_injector import providers as di
from dependency.core import Container, Entrypoint
from dependency.core.injection import ProviderInjection
from dependency.core.utils.threading import handle_exit
from example.plugin.runtime.clock import Clock
from example.plugin.runtime.modes import StationMode
from example.plugin.runtime.state import StationState
from example.plugin.sensors import SensorsPlugin
from example.plugin.sensors.sampler import Sampler
from example.plugin.storage.store import ReadingStore
from example.app.main.plugins import PLUGINS

_logger = logging.getLogger("station")


async def _drain() -> None:
    """Yield to the loop so already-scheduled event deliveries can finish."""
    await asyncio.sleep(0)

# Resolved against the package, not the working directory: a unit started by systemd
# from / must find its config, and a test must not depend on where pytest was invoked.
DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config.json"


class MonitoringStation(Entrypoint):
    """A sensor station: samples on a cadence, stores, and raises alerts.

    The three-step startup is load-bearing and must stay in this order:

      1. super().__init__ builds the structural tree and resolves plugin config.
      2. importing app.main.imports runs every @instance decorator, which is what
         registers the implementations.
      3. super().initialize() expands the graph, wires it, and bootstraps.

    Move the import to the top of the file and nothing is registered in time; the
    error will not explain that.
    """

    def __init__(self, config_file: Optional[str] = None) -> None:
        container = Container.from_json(
            config_file or str(DEFAULT_CONFIG), required=True)
        super().__init__(container, PLUGINS)

        import example.app.main.imports  # noqa: F401 - registers implementations

        super().initialize()
        self.__clock: Clock = Clock.provide()
        self.__sampler: Sampler = Sampler.provide()
        self.__state: StationState = StationState.provide()
        self.__store: ReadingStore = ReadingStore.provide()

        # Sequenced here, not in a bootstrap: every subscriber is registered by now.
        self.__sampler.warmup()

    @property
    def state(self) -> StationMode:
        return self.__state.state

    @property
    def store(self) -> ReadingStore:
        return self.__store

    def run(self, cycles: Optional[int] = None) -> None:
        """Sample until stopped, or for a fixed number of cycles.

        `cycles` is what makes the station testable: the same loop that runs forever
        on the unit runs three times under pytest.
        """
        interval = SensorsPlugin.config.sensors.sample_interval_s
        remaining = cycles
        while remaining is None or remaining > 0:
            for reading in self.__sampler.sample_once():
                _logger.info("sample %s", reading)
            self.__clock.sleep(interval)
            if remaining is not None:
                remaining -= 1

    @handle_exit
    def main_loop(self) -> None:
        """Entry point for the unit. Ctrl-C exits through handle_exit."""
        try:
            self.run()
        finally:
            self.stop()

    def stop(self) -> None:
        """Shut down resource-backed providers and the async loop.

        The application has to do this itself. Measured: the root Container's own
        .providers is just ['__self__'] because plugin providers live in nested
        sub-containers, so container.shutdown_resources() reaches none of them. See
        D-034.
        """
        self.__state.transition(StationMode.STOPPED)

        # Events are published with create_task, so anything raised by the last sample
        # may still be in flight. Give it a moment before the loop goes away.
        from example.plugin.runtime.deferred import DeferredService
        deferred: DeferredService = DeferredService.provide()
        deferred.run(_drain(), timeout=1.0)

        for injection in self.__resource_providers():
            injection.provider.shutdown()  # type: ignore[attr-defined]

        deferred.shutdown()

    def __resource_providers(self) -> list[ProviderInjection]:
        return [
            injection
            for plugin in self.modules
            for injection in plugin.collect_providers()
            if isinstance(injection.provider, di.Resource)
        ]
