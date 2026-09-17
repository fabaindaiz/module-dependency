from dependency.core import component
from dependency.library.components import ObserverComponent
from example.plugin.hardware import HardwarePlugin
from example.plugin.hardware.events import HardwareEventContext

@component(
    module=HardwarePlugin,
)
class HardwareObserver(ObserverComponent[HardwareEventContext]):
    """Publishes hardware events. The contract comes from the library; the module,
    the provider and the context type stay here, where the domain is."""
