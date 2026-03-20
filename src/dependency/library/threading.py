import logging
import threading
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

logger = logging.getLogger("ThreadHelper")
WRAP = TypeVar('WRAP', bound=Callable[..., Any])

def excluded(blocking: bool = False, default: Any = None) -> Callable[[WRAP], WRAP]:
    def function(func: WRAP) -> WRAP:
        lock = threading.Lock()
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if lock.acquire(blocking=blocking):
                try:
                    return func(*args, **kwargs)
                finally:
                    lock.release()
            else:
                return default
        return wrapper # type: ignore
    return function

def threaded(name: Optional[str] = None, daemon: bool = True) -> Callable[[WRAP], WRAP]:
    def function(func: WRAP) -> WRAP:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            _thread = threading.Thread(target=func, args=args, kwargs=kwargs, name=name)
            _thread.daemon = daemon
            _thread.start()
            logger.debug(f"Funcion '{func.__module__}.{func.__name__}' running on a thread (daemon={daemon}) ")
        return wrapper # type: ignore
    return function

def handle_exit(func: WRAP) -> WRAP:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, exiting...")
            import os
            os._exit(1)
    return wrapper # type: ignore
