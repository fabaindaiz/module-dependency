from dependency.core import provider, providers
from typing import Callable
from example.plugin.hardware.observer import HardwareObserver, HardwareObserverComponent
from example.plugin.hardware.observer.interfaces import EventSubscriber, HardwareEventContext
from library.mixin.observer import EventPublisher

@provider(
    component=HardwareObserverComponent,
    provider = providers.Singleton
)
class HardwareObserverA(HardwareObserver):
    def __init__(self, config: dict):
        self.__publisher = EventPublisher()
        print("PublisherObserverA initialized")

    def subscribe(self, listener: type[EventSubscriber]) -> Callable:
        return self.__publisher.subscribe(listener)

    def update(self, context: HardwareEventContext) -> None:
        self.__publisher.update(context)