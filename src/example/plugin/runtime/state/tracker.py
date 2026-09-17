import logging
from dependency.core import instance, providers
from dependency.library.components import StateMixin
from example.plugin.runtime.modes import StationMode
from example.plugin.runtime.state import StationState

_logger = logging.getLogger("station.runtime")


@instance(
    provider=providers.Singleton,
)
class LoggingStationState(StateMixin[StationMode], StationState):
    """Announces every transition.

    This is why the contract has transition() instead of a settable attribute: a move
    between states is worth seeing, and a plain setter gives you nowhere to stand.
    """

    def initial_state(self) -> StationMode:
        return StationMode.STARTING

    def transition(self, state: StationMode) -> None:
        previous = self.state
        if previous is state:
            return
        _logger.info("station %s -> %s", previous.value, state.value)
        super().transition(state)
