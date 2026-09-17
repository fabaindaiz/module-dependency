from dependency.core import component
from dependency.library.components import StateComponent
from example.plugin.runtime import RuntimePlugin
from example.plugin.runtime.modes import StationMode

@component(
    module=RuntimePlugin,
)
class StationState(StateComponent[StationMode]):
    """The station's lifecycle state.

    The contract comes from dependency.library.components; what stays here is the
    module, the provider, and the domain's own StationMode.
    """
