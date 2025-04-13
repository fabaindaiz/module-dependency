from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

T = TypeVar('T', bound='EventContext')

class EventContext(ABC):
    pass

class EventListener(ABC, Generic[T]):
    @property
    def context(self) -> type:
        return T
    
    def listen(self, callback: Callable[[T], None]) -> None:
        pass

    @abstractmethod
    def update(self, context: T) -> None:
        pass


class EventPublisher():
    def __init__(self):
        self.__targets: dict[type[EventContext], list[EventListener]] = {}
        pass

    def subscribe(self, listener: EventListener) -> None:
        pass
    pass





if __name__ == '__main__':
    pass