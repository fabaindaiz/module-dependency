from abc import ABC, abstractmethod
from dependency.core import Component, component
from typing import Callable
from example.plugins.hardware.observer.interfaces import HardwareEventContext, EventSubscriber

class HardwareObserver(ABC):
    @abstractmethod
    def subscribe(self, listener: type[EventSubscriber]) -> Callable:
        pass

    @abstractmethod
    def update(self, context: HardwareEventContext) -> None:
        pass

@component(
    interface=HardwareObserver
)
class HardwareObserverComponent(Component):
    pass