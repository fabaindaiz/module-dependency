from dependency.core.exceptions import ResolutionError as ResolutionError
from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.utils.cycle import find_cycles as find_cycles
from typing import Iterable

def raise_circular_error(providers: Iterable[Injectable]) -> bool:
    """Raise an error if circular dependencies are detected.

    Args:
        providers (Iterable[Injectable]): The set of injectables to check for cycles.

    Returns:
        bool: True if cycles were detected and errors were raised, False otherwise.
    """
def raise_dependency_error(unresolved: Iterable[Injectable]) -> bool:
    """Raise an error when unresolved dependencies are detected.

    Args:
        unresolved (Iterable[Injectable]): The set of unresolved injectables.

    Returns:
        bool: True if unresolved dependencies were detected and errors were raised, False otherwise.
    """
def raise_resolution_error(providers: Iterable[Injectable], unresolved: Iterable[Injectable]) -> None:
    """Raise an error if unresolved provider imports are detected.

    Args:
        providers (Iterable[Injectable]): The set of injectables to check.
        unresolved (Iterable[Injectable]): The set of resolved providers to check against.

    Raises:
        ResolutionError: If unresolved dependencies or cycles are detected.
    """
