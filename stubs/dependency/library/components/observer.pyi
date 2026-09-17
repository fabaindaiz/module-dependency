import abc
from abc import abstractmethod
from dependency.core import Component as Component
from dependency.library.patterns.observer import EventContext as EventContext, EventPublisher as EventPublisher, EventSubscriber as EventSubscriber
from typing import Any, Callable, Generic, TypeVar

CONTEXT = TypeVar('CONTEXT', bound=EventContext)
SubscribeDecorator = Callable[[Callable[[Any], Any]], Callable[[Any], Any]]

class ObserverComponent(Component, Generic[CONTEXT], metaclass=abc.ABCMeta):
    """Contract for a component that publishes events to subscribers.

    Not decorated: the application declares its own component from this base, which
    keeps the module, provider and import declarations where they belong and lets the
    context type stay domain-specific.

    Parameterise it with the domain's own `EventContext` subclass so that `update` is
    typed to that domain rather than to the generic base::

        @component(module=HardwarePlugin)
        class HardwareObserver(ObserverComponent[HardwareEventContext]):
            pass

    Pair it with `EventPublisherMixin` on the implementation to inherit the publisher
    plumbing, leaving only the dispatch policy to write.
    """
    @abstractmethod
    def subscribe(self, listener: type[EventSubscriber]) -> SubscribeDecorator:
        """Register a listener, returning the decorator that binds the callback."""
    @abstractmethod
    def update(self, context: CONTEXT) -> None:
        """Dispatch an event to the subscribers.

        Dispatch policy is deliberately left to the implementation: publishing is a
        coroutine, so whether it is awaited, scheduled on a task loop or run in a
        thread pool is an application decision, not a library one.
        """

class EventPublisherMixin(Generic[CONTEXT]):
    """Implementation body for an `ObserverComponent`.

    Supplies the publisher and `subscribe`. It does **not** implement `update`, because
    `EventPublisher.update` is a coroutine and how it is driven is the part that differs
    between applications — see `publish` for the raw coroutine.

    Mix it in ahead of the component so its `__init__` runs::

        @instance(imports=[DeferredService], provider=providers.Singleton)
        class HardwareObserverA(EventPublisherMixin[HardwareEventContext], HardwareObserver):
            def update(self, context: HardwareEventContext) -> None:
                DeferredService.provide().run(self.publish(context))
    """
    def __init__(self, **kwargs: Any) -> None: ...
    def subscribe(self, listener: type[EventSubscriber]) -> SubscribeDecorator:
        """Register a listener against this instance's publisher."""
    async def publish(self, context: CONTEXT) -> None:
        """Await delivery to every subscriber of this context's type."""
