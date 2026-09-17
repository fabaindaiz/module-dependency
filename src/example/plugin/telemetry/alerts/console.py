import logging
from typing import Optional
from dependency.core import DependencyError, instance, providers
from dependency.library.patterns.observer import EventSubscriber
from example.plugin.display.panel import StatusPanel
from example.plugin.telemetry import TelemetryPlugin
from example.plugin.telemetry.alerts import AlertSink
from example.plugin.telemetry.events import ThresholdExceeded
from example.plugin.telemetry.observer import StationObserver

_logger = logging.getLogger("station.telemetry")


@instance(
    imports=[StationObserver],
    optional=[StatusPanel],
    provider=providers.Singleton,
    bootstrap=True,
)
class ConsoleAlertSink(AlertSink):
    """Logs every breach, and mirrors it to the panel when a panel exists.

    StatusPanel is declared under `optional=`, not `imports=`. The difference is the
    whole reason this framework exists:

      - `imports=[StatusPanel]` would mean the station refuses to start on any unit
        built without a screen.
      - `optional=[StatusPanel]` means the panel is resolved and wired when the
        display plugin is loaded, and silently skipped when it is not. The alert path
        keeps working either way, and no failure cascades from its absence.

    Run `hatch run build:example` with and without DisplayPlugin in plugins.py to see
    the same station come up both ways.

    bootstrap=True so the subscription is registered at startup, before the sampler's
    warm-up publishes anything.
    """

    def __init__(self) -> None:
        self.__prefix = TelemetryPlugin.config.telemetry.alert_prefix
        self.__panel: Optional[StatusPanel] = self.__find_panel()

        observer: StationObserver = StationObserver.provide()

        @observer.subscribe(EventSubscriber)
        async def on_threshold(event: ThresholdExceeded) -> None:
            self.raise_alert(event)

    @staticmethod
    def __find_panel() -> Optional[StatusPanel]:
        """Resolve the panel if this unit has one.

        An optional dependency that was not resolved raises DeclarationError from
        .provide(); that is the signal it is absent, not a failure to handle.
        """
        try:
            panel: StatusPanel = StatusPanel.provide()
            return panel
        except DependencyError:
            _logger.info("no status panel on this unit; alerts go to the log only")
            return None

    def raise_alert(self, event: ThresholdExceeded) -> None:
        line = (
            f"{self.__prefix} {event.reading.sensor} "
            f"{event.reading.value:.1f} > {event.limit:.1f}"
        )
        _logger.warning(line)
        if self.__panel is not None:
            self.__panel.show(line)
