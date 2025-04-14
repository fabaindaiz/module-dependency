from dependency.core import provider, providers
from typing import Callable
from example.plugins.module1.observer import Observer, ObserverComponent
from example.plugins.module1.observer.interfaces import EventSubscriber, ObserverEventContext
from library.mixins.observer import EventPublisher

@provider(
    component=ObserverComponent,
    provider = providers.Singleton
)
class PublisherObserverA(Observer):
    def __init__(self, config: dict):
        self.__publisher = EventPublisher()
        print("PublisherObserverA initialized")

    def subscribe(self, listener: type[EventSubscriber]) -> Callable:
        return self.__publisher.subscribe(listener)

    def update(self, context: ObserverEventContext) -> None:
        self.__publisher.update(context)