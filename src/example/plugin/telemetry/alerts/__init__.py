from abc import abstractmethod
from dependency.core import Component, component
from example.plugin.telemetry import TelemetryPlugin
from example.plugin.telemetry.events import ThresholdExceeded


@component(
    module=TelemetryPlugin,
)
class AlertSink(Component):
    """Where an exceeded threshold ends up."""

    @abstractmethod
    def raise_alert(self, event: ThresholdExceeded) -> None:
        """Report one threshold breach."""
