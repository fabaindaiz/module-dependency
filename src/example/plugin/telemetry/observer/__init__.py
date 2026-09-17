from dependency.core import component
from dependency.library.components import ObserverComponent
from example.plugin.telemetry import TelemetryPlugin
from example.plugin.telemetry.events import StationEvent

@component(
    module=TelemetryPlugin,
)
class StationObserver(ObserverComponent[StationEvent]):
    """The station's event bus.

    Contract from the library; the module, the provider and StationEvent stay here.
    """
