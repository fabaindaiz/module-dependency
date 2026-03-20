from concurrent.futures import Future
from typing import TypeVar

T = TypeVar('T')

class InmediateFuture(Future[T]):
    """A Future that is already completed with a given result.

    Args:
        result (T): The result to set for the Future.
    """
    def __init__(self, result: T) -> None:
        super().__init__()
        self.set_result(result)
