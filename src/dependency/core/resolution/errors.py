import logging
from dependency.core.injection.injectable import Injectable
from dependency.core.exceptions import ResolutionError
from dependency.core.utils.cycle import find_cycles
_logger = logging.getLogger("dependency.loader")

def raise_circular_error(
    providers: list[Injectable]
) -> bool:
    """Raise an error if circular dependencies are detected.

    Args:
        providers (list[Injectable]): The list of injectables to check for cycles.

    Returns:
        bool: True if cycles were detected and errors were raised, False otherwise.
    """
    cycles = find_cycles(lambda i: i.imports, providers)
    for cycle in cycles:
        _logger.error(f"Circular dependency detected: {cycle}")
    return len(cycles) > 0

def raise_dependency_error(
    unresolved: list[Injectable],
) -> bool:
    """Raise an error when unresolved dependencies are detected.

    Args:
        unresolved (list[Injectable]): The list of unresolved injectables.

    Returns:
        bool: True if unresolved dependencies were detected and errors were raised, False otherwise.
    """
    for injectable in unresolved:
        unresolved_imports = filter(lambda d: not d.is_resolved, injectable.imports)
        _logger.error(f"Injectable {injectable} has unresolved dependencies: {list(unresolved_imports)}")
    return len(unresolved) > 0

def raise_resolution_error(
    providers: list[Injectable],
    unresolved: list[Injectable],
) -> None:
    """Raise an error if unresolved provider imports are detected.

    Args:
        providers (list[Injectable]): The list of injectables to check.
        unresolved (list[Injectable]): The resolved providers to check against.

    Raises:
        ResolutionError: If unresolved dependencies or cycles are detected.
    """
    circular_error = raise_circular_error(providers)
    dependency_error = raise_dependency_error(unresolved)
    if circular_error or dependency_error:
        raise ResolutionError(f"Provider resolution failed due to dependency errors: {unresolved}")
