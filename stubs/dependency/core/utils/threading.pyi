from typing import Any, Callable, TypeVar

WRAP = TypeVar('WRAP', bound=Callable[..., Any])

def handle_exit(func: WRAP) -> WRAP:
    """Exit the process cleanly on KeyboardInterrupt.

    Lives in core/utils rather than in library/ so that core does not depend on
    library: library imports from core, never the other way round. See D-019.
    """
