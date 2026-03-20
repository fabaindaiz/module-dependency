import asyncio
from typing import Any, Callable, TypeVar

CONTEXT = TypeVar('CONTEXT', bound='EventContext')

class EventContext:
    pass

class EventSubscriber:
    def __init__(self,
        callback: Callable[..., Any]
    ) -> None:
        self.callback: Callable[..., Any] = callback

    async def update(self, context: EventContext) -> None:
        await self.callback(context)

class EventPublisher:
    def __init__(self) -> None:
        self.__targets: dict[type[EventContext], list[EventSubscriber]] = {}

    def subscribe(self, subscriber: type[EventSubscriber]) -> Callable[[Callable[[CONTEXT], Any]], Callable[[CONTEXT], Any]]:
        def wrapper(func: Callable[[CONTEXT], Any]) -> Callable[[CONTEXT], Any]:
            if len(func.__annotations__) == 0:
                raise TypeError(f"Function '{func.__name__}' must have at least one parameter with a type annotation that is a subclass of EventContext.")
            name, value = next(iter(func.__annotations__.items()))
            if name == "return":
                raise TypeError(f"Function '{func.__name__}' must have at least one parameter with a type annotation that is a subclass of EventContext.")
            if not issubclass(value, EventContext):
                raise TypeError(f"Parameter '{name}' in '{func.__name__}' must be a subclass of EventContext, got {value.__name__}.")

            self.__targets.setdefault(value, []).append(subscriber(func))
            return func
        return wrapper

    async def update(self, context: EventContext) -> None:
        subscribers = self.__targets.get(type(context), [])
        async with asyncio.TaskGroup() as tg:
            for subscriber in subscribers:
                tg.create_task(subscriber.update(context))


if __name__ == '__main__':
    class EventA(EventContext):
        def __init__(self, parameter: str) -> None:
            self.parameterA = parameter

    class EventB(EventContext):
        def __init__(self, parameter: str) -> None:
            self.parameterB = parameter

    class Observer():
        def __init__(self) -> None:
            self.publisher = EventPublisher()

            @self.publisher.subscribe(EventSubscriber)
            async def listen_event_a(context1: EventA) -> None:
                print(f"Event A triggered with parameter: {context1.parameterA}")

            @self.publisher.subscribe(EventSubscriber)
            async def listen_event_b(context2: EventB) -> None:
                print(f"Event B triggered with parameter: {context2.parameterB}")

    async def execute() -> None:
        instance = Observer()
        await instance.publisher.update(EventA("Hello World!"))
        await instance.publisher.update(EventB("Goodbye World!"))

    asyncio.run(execute())
