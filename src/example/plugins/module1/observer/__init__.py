from abc import ABC, abstractmethod
from dependency.core import Component, component
from typing import Callable
from example.plugins.module1.observer.interfaces import ObserverEventContext, EventSubscriber

class Observer(ABC):
    @abstractmethod
    def subscribe(self, listener: type[EventSubscriber]) -> Callable:
        pass

    @abstractmethod
    def update(self, context: ObserverEventContext) -> None:
        pass

@component(
    interface=Observer
)
class ObserverComponent(Component):
    pass