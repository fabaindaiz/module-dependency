from typing import Generic, TypeVar

T = TypeVar('T')

class StateMixin(Generic[T]):
    def __init__(self, initial_state: T, **kwargs) -> None: ...
    @property
    def state(self) -> T: ...
    @state.setter
    def state(self, state: T) -> None: ...
