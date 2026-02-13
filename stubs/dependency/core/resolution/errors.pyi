from dependency.core.exceptions import ResolutionError as ResolutionError
from dependency.core.injection.resoluble import ResolubleProvider as ResolubleProvider
from dependency.core.utils.cycle import find_cycles as find_cycles

def raise_circular_error(providers: list[ResolubleProvider]) -> bool:
    """Raise an error if circular dependencies are detected.

    Args:
        providers (list[ResolubleClass]): The list of resoluble classes to check for cycles.

    Returns:
        bool: True if cycles were detected and errors were raised, False otherwise.
    """
def raise_dependency_error(unresolved: list[ResolubleProvider]) -> bool:
    """Raise an error when unresolved dependencies are detected.

    Args:
        unresolved (list[ResolubleClass]): The list of unresolved resoluble classes.

    Returns:
        bool: True if unresolved dependencies were detected and errors were raised, False otherwise.
    """
def raise_resolution_error(providers: list[ResolubleProvider], unresolved: list[ResolubleProvider]) -> None:
    """Raise an error if unresolved provider imports are detected.

    Args:
        providers (list[ProviderInjection]): The list of provider injections to check.
        unresolved (list[ProviderInjection]): The resolved providers to check against.

    Raises:
        ResolutionError: If unresolved dependencies or cycles are detected.
    """
