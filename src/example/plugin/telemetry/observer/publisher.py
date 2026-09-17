from dependency.core import instance, providers
from dependency.library.components import EventPublisherMixin
from example.plugin.runtime.deferred import DeferredService
from example.plugin.telemetry.events import StationEvent
from example.plugin.telemetry.observer import StationObserver


@instance(
    imports=[DeferredService],
    provider=providers.Singleton,
)
class DeferredStationObserver(EventPublisherMixin[StationEvent], StationObserver):
    """Publishes without blocking the sampler.

    The mixin supplies the publisher and subscribe(); only the dispatch policy is
    written here. Delivery is a coroutine, and the sampling loop is the thing with a
    deadline, so it is scheduled on the deferred service rather than awaited inline.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__deferred: DeferredService = DeferredService.provide()

    def update(self, context: StationEvent) -> None:
        self.__deferred.create_task(self.publish(context))
