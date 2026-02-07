from abc import ABC, abstractmethod
from typing import Callable
from dependency.core import Component, component
from example.plugin.hardware import HardwarePlugin
from example.plugin.hardware.events import EventSubscriber, HardwareEventContext

@component(
    module=HardwarePlugin,
)
class HardwareObserver(ABC, Component):
    @abstractmethod
    def subscribe(self, listener: type[EventSubscriber]) -> Callable:
        pass

    @abstractmethod
    def update(self, context: HardwareEventContext) -> None:
        pass
