from dependency.core.utils.threading import handle_exit as handle_exit
from typing import Any, Callable, TypeVar

__all__ = ['handle_exit', 'excluded', 'threaded']

WRAP = TypeVar('WRAP', bound=Callable[..., Any])

def excluded(blocking: bool = False, default: Any = None) -> Callable[[WRAP], WRAP]: ...
def threaded(name: str | None = None, daemon: bool = True) -> Callable[[WRAP], WRAP]: ...
