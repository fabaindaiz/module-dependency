from typing import Callable
from dependency.core import instance, providers
from example.plugin.hardware.events import EventSubscriber, HardwareEventContext
from example.plugin.hardware.observer import HardwareObserver, HardwareObserverComponent
from library.mixin.observer import EventPublisher

@instance(
    component=HardwareObserverComponent,
    provider=providers.Singleton,
)
class HardwareObserverA(HardwareObserver):
    def __init__(self):
        self.__publisher = EventPublisher()
        print("PublisherObserverA initialized")

    def subscribe(self, listener: type[EventSubscriber]) -> Callable:
        return self.__publisher.subscribe(listener)

    def update(self, context: HardwareEventContext) -> None:
        self.__publisher.update(context)
