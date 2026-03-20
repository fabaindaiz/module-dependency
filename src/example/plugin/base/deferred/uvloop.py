import asyncio
import uvloop
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Coroutine, Optional, TypeVar
from dependency.core import instance, providers
from dependency.library.threading import threaded
from example.plugin.base.deferred import DeferredService

T = TypeVar('T')

@instance(
    provider=providers.Singleton,
    bootstrap=True,
)
class UVLoopDeferredService(DeferredService):
    def __init__(self) -> None:
        self.__thread_pool = ThreadPoolExecutor(max_workers=4)
        self.__running_loop: asyncio.AbstractEventLoop = uvloop.new_event_loop()
        self.start_event_loop()

    @property
    def event_loop(self) -> asyncio.AbstractEventLoop:
        return self.__running_loop

    @property
    def thread_pool(self) -> ThreadPoolExecutor:
        return self.__thread_pool

    def create_task(self, coro: Coroutine[None, None, T]) -> Future[T]:
        return asyncio.run_coroutine_threadsafe(coro, self.__running_loop)

    def run(self, coro: Coroutine[None, None, T], timeout: Optional[float] = None) -> T:
        return self.create_task(coro).result(timeout=timeout)

    async def run_in_executor(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        def wrapper() -> T:
            return func(*args, **kwargs)
        return await self.__running_loop.run_in_executor(self.__thread_pool, wrapper)

    @threaded()
    def start_event_loop(self) -> None:
        """Event Loop runner loop.
           Note: This method needs to run in a separate thread.
        """
        asyncio.set_event_loop(self.__running_loop)
        self.__running_loop.set_default_executor(self.__thread_pool)
        self.__running_loop.run_forever()
