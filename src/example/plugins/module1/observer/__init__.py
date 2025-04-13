from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugins.module1.observer.interfaces import Event, EventListener, EventContext

class Observer(ABC):
    @abstractmethod
    def subscribe(self, listener: EventListener) -> None:
        pass

    @abstractmethod
    def unsubscribe(self, listener: EventListener) -> None:
        pass

    @abstractmethod
    def notify(self, context: EventContext) -> None:
        pass

@component(
    interface=Observer
)
class ObserverComponent(Component):
    pass