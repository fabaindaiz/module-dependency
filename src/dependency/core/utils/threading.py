import logging
from functools import wraps
from typing import Any, Callable, TypeVar

_logger = logging.getLogger("dependency.loader")
WRAP = TypeVar('WRAP', bound=Callable[..., Any])

def handle_exit(func: WRAP) -> WRAP:
    """Exit the process cleanly on KeyboardInterrupt.

    Lives in core/utils rather than in library/ so that core does not depend on
    library: library imports from core, never the other way round. See D-019.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            _logger.info("Received keyboard interrupt, exiting...")
            import os
            os._exit(1)
    return wrapper # type: ignore
