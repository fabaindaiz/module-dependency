from abc import abstractmethod
from typing import Any, Generic, TypeVar
from dependency.core import Component
from dependency.library.patterns.state import StateHolder

STATE = TypeVar("STATE")


class StateComponent(Component, Generic[STATE]):
    """Contract for a component that owns one piece of mutable state.

    Not decorated: the application declares its own component from this base.

    Parameterise it with the domain's own state type — an enum, a dataclass, or a
    hierarchy of state classes::

        @component(module=RuntimePlugin)
        class StationState(StateComponent[StationMode]):
            pass

    `transition` exists rather than a plain setter because a state change is usually
    worth observing: an implementation can log it, publish an event, or reject an
    illegal move. A bare attribute cannot.
    """

    @abstractmethod
    def initial_state(self) -> STATE:
        """The state this component starts in. Called once, during construction."""

    @property
    @abstractmethod
    def state(self) -> STATE:
        """The current state."""

    @abstractmethod
    def transition(self, state: STATE) -> None:
        """Move to a new state."""


class StateMixin(Generic[STATE]):
    """Implementation body for a `StateComponent`.

    Supplies storage over a `StateHolder` and an unconditional `transition`. The
    concrete class provides `initial_state`, and overrides `transition` when a move
    needs to be validated or announced::

        @instance(provider=providers.Singleton)
        class StationStateImpl(StateMixin[StationMode], StationState):
            def initial_state(self) -> StationMode:
                return StationMode.STARTING
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._holder: StateHolder[STATE] = StateHolder(self.initial_state())

    @abstractmethod
    def initial_state(self) -> STATE:
        """Provided by the concrete class."""

    @property
    def state(self) -> STATE:
        return self._holder.state

    def transition(self, state: STATE) -> None:
        self._holder.state = state
