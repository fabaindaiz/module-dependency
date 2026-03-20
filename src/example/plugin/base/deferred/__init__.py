import asyncio
from abc import ABC, abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Coroutine, Optional, TypeVar
from dependency.core import Component, component
from example.plugin.base import BasePlugin

T = TypeVar('T')

@component(
    module=BasePlugin,
)
class DeferredService(ABC, Component):
    """DeferredService

       Deferred Service is an abstract class that defines the methods to interact with asyncio tasks.
    """
    @property
    @abstractmethod
    def event_loop(self) -> asyncio.AbstractEventLoop:
        """Get the running event loop. Use for advanced asyncio operations.

        Returns:
            asyncio.AbstractEventLoop: The running event loop.
        """
        pass

    @property
    @abstractmethod
    def thread_pool(self) -> ThreadPoolExecutor:
        """Get the thread pool executor. Use for short-live blocking operations.

        Returns:
            ThreadPoolExecutor: The thread pool executor.
        """
        pass

    @abstractmethod
    def create_task(self, coro: Coroutine[None, None, T]) -> Future[T]:
        """Create an asynchronous task. Please do not block the event loop.

        Args:
            coro (Coroutine): The coroutine to be executed as a task.

        Returns:
            The future object representing the asynchronous task.
        """
        pass

    @abstractmethod
    def run(self, coro: Coroutine[None, None, T], timeout: Optional[float] = None) -> T:
        """Run an asynchronous task. Please do not block the event loop.

        Args:
            coro (Coroutine): The coroutine to be executed and waited as a task.
            timeout (Optional[float]): The timeout for waiting the task. If None, wait indefinitely.

        Returns:
            The result of the coroutine execution.
        """
        pass

    @abstractmethod
    async def run_in_executor(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Run a function in the thread pool executor. Use for short-live blocking operations.

        Args:
            func (Callable): The function to be executed in the thread pool executor.
            *args: The arguments to be passed to the function.
            **kwargs: The keyword arguments to be passed to the function.

        Returns:
            The result of the function execution.
        """
        pass

    @abstractmethod
    def start_event_loop(self) -> None:
        """Start the asynchronous task loop.
        """
        pass
