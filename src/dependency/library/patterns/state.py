from typing import Any, Generic, TypeVar

T = TypeVar('T')

class StateHolder(Generic[T]):
    def __init__(self, initial_state: T, **kwargs: Any):
        super().__init__(**kwargs)
        self.__state: T = initial_state

    @property
    def state(self) -> T:
        return self.__state

    @state.setter
    def state(self, state: T) -> None:
        self.__state = state
