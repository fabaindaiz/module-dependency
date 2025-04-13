from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T', bound='EventContext')

class EventContext(ABC):
    pass

class EventListener(ABC, Generic[T]):
    @property
    def context(self) -> type:
        return T

    @abstractmethod
    def update(self, context: EventContext) -> None:
        pass