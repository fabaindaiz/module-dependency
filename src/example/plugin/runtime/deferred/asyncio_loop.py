import asyncio
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Coroutine, Optional, TypeVar
from dependency.core import instance, providers
from dependency.library.threading import threaded
from example.plugin.runtime import RuntimePlugin
from example.plugin.runtime.deferred import DeferredService

T = TypeVar("T")


@instance(
    provider=providers.Singleton,
    bootstrap=True,
)
class AsyncioDeferredService(DeferredService):
    """Standard-library implementation. No third-party dependency.

    bootstrap=True because the loop has to be turning before anything schedules on it:
    the first telemetry event is published during the warm-up samples, which happen
    while the rest of the graph is still being initialised. Without it, the service
    would only start when something first called .provide() — too late.
    """

    def __init__(self) -> None:
        workers = RuntimePlugin.config.runtime.thread_pool_workers
        self.__thread_pool = ThreadPoolExecutor(max_workers=workers)
        self.__running_loop = asyncio.new_event_loop()
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

    async def run_in_executor(
        self, func: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        def wrapper() -> T:
            return func(*args, **kwargs)

        return await self.__running_loop.run_in_executor(self.__thread_pool, wrapper)

    def shutdown(self) -> None:
        self.__running_loop.call_soon_threadsafe(self.__running_loop.stop)
        self.__thread_pool.shutdown(wait=False)

    @threaded()
    def start_event_loop(self) -> None:
        """Run the loop. Must be on its own thread: it never returns."""
        asyncio.set_event_loop(self.__running_loop)
        self.__running_loop.set_default_executor(self.__thread_pool)
        self.__running_loop.run_forever()
