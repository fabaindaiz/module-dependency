from abc import ABC, abstractmethod
from threading import Thread
from typing import Callable, Generic, TypeVar

T = TypeVar('T', bound='EventContext')

class EventContext(ABC):
    pass

class EventSubscriber(ABC, Generic[T]):
    def __init__(self, callback: Callable[[T], None]) -> None:
        self.callback: Callable[[T], None] = callback

    @property
    def context(self) -> type:
        return self.callback.__annotations__.get('context', None) # type: ignore

    def update(self, context: T) -> None:
        self.callback(context)


class EventThreadingSubscriber(EventSubscriber[T], Generic[T]):
    def update(self, context: T) -> None:
        Thread(target=self.callback, args=(context,), daemon=True).start()

class EventPublisher():
    def __init__(self) -> None:
        self.__targets: dict[type[EventContext], list[EventSubscriber]] = {}
        pass

    def subscribe(self, listener: type[EventSubscriber]) -> Callable:
        def wrapper(func: Callable[[EventContext], None]) -> Callable[[EventContext], None]:
            instance = listener(func)
            self.__targets.setdefault(instance.context, []).append(instance)
            return func
        return wrapper
    
    def update(self, context: EventContext) -> None:
        listeners = self.__targets.get(type(context), [])
        for listener in listeners:
            listener.update(context)


if __name__ == '__main__':
    class EventA(EventContext):
        def __init__(self, parameter: str) -> None:
            self.parameter = parameter
    
    class EventSubscriberA(EventSubscriber[EventA]):
        pass

    class EventB(EventContext):
        def __init__(self, parameter: str) -> None:
            self.parameter = parameter
    
    class EventSubscriberB(EventThreadingSubscriber[EventB]):
        pass

    class Example():
        def __init__(self) -> None:
            self.publisher = EventPublisher()

            @self.publisher.subscribe(EventSubscriberA)
            def listen_event_a(context: EventA) -> None:
                print(f"Event A triggered with parameter: {context.parameter}")
            
            @self.publisher.subscribe(EventSubscriberB)
            def listen_event_b(context: EventB) -> None:
                print(f"Event B triggered with parameter: {context.parameter}")
        
    instance = Example()
    instance.publisher.update(EventA("Hello World!"))
    instance.publisher.update(EventB("Goodbye World!"))