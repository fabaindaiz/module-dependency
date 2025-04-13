from dependency.core import dependent
from typing import Callable
from example.plugins.module1.observer.interfaces import EventContext, EventListener

class EventContextA(EventContext):
    def __init__(self, parameter: str):
        self.parameter = parameter

@dependent()
class EventListenerA(EventListener[EventContextA]):
    def listen(callback: Callable[[EventContextA] ,None]):
        pass

    @staticmethod
    def fabricate() -> EventContextA:
        return EventContextA()

    def update(self, context: EventContextA) -> None:
        self.listen_event_a(context.parameter)

    def listen_event_a(self, parameter: str) -> None:
        pass