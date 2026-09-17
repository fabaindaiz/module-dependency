import asyncio
from abc import abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Coroutine, Optional, TypeVar
from dependency.core import Component, component
from example.plugin.runtime import RuntimePlugin

T = TypeVar('T')

@component(
    module=RuntimePlugin,
)
class DeferredService(Component):
    """Somewhere to run coroutines and blocking calls without stalling the station.

    The sampling loop is synchronous and must stay that way — it is the thing with a
    deadline. Anything that can wait goes through here.
    """
    @property
    @abstractmethod
    def event_loop(self) -> asyncio.AbstractEventLoop:
        """The running loop, for advanced asyncio work."""

    @property
    @abstractmethod
    def thread_pool(self) -> ThreadPoolExecutor:
        """The executor, for short-lived blocking calls."""

    @abstractmethod
    def create_task(self, coro: Coroutine[None, None, T]) -> Future[T]:
        """Schedule a coroutine and return immediately."""

    @abstractmethod
    def run(self, coro: Coroutine[None, None, T], timeout: Optional[float] = None) -> T:
        """Schedule a coroutine and wait for its result."""

    @abstractmethod
    async def run_in_executor(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Run a blocking function off the event loop."""

    @abstractmethod
    def shutdown(self) -> None:
        """Stop the loop and drain the pool. Called once, on the way out."""
