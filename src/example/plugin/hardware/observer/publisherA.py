from dependency.core import instance, providers
from dependency.library.components import EventPublisherMixin
from example.plugin.base.deferred import DeferredService
from example.plugin.hardware.events import HardwareEventContext
from example.plugin.hardware.observer import HardwareObserver

@instance(
    imports=[
        DeferredService,
    ],
    provider=providers.Singleton,
)
class HardwareObserverA(EventPublisherMixin[HardwareEventContext], HardwareObserver):
    """The mixin supplies the publisher and subscribe(); only the dispatch policy is
    written here, because how the coroutine is driven is an application decision."""
    def __init__(self) -> None:
        super().__init__()
        self.__deferred: DeferredService = DeferredService.provide()
        print("PublisherObserverA initialized")

    def update(self, context: HardwareEventContext) -> None:
        self.__deferred.run(self.publish(context))
