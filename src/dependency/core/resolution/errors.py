import logging
from typing import Iterable
from dependency.core.injection.injection import ProviderInjection
from dependency.core.exceptions import ResolutionError
from dependency.core.utils.cycle import find_cycles
_logger = logging.getLogger("dependency.loader")

def raise_circular_error(
    providers: Iterable[ProviderInjection]
) -> bool:
    cycles = find_cycles(lambda i: i.imports, providers)
    for cycle in cycles:
        _logger.error(f"Circular dependency detected: {cycle}")
    return len(cycles) > 0

def raise_dependency_error(
    unresolved: Iterable[ProviderInjection],
) -> bool:
    for provider in unresolved:
        unresolved_imports = filter(lambda d: not d.is_resolved, provider.imports)
        _logger.error(f"Provider {provider} has unresolved dependencies: {list(unresolved_imports)}")
        return True
    return False

def raise_resolution_error(
    providers: Iterable[ProviderInjection],
    unresolved: Iterable[ProviderInjection],
) -> None:
    unresolved_list: list[ProviderInjection] = list(unresolved)
    circular_error = raise_circular_error(providers)
    dependency_error = raise_dependency_error(unresolved)
    if circular_error or dependency_error:
        raise ResolutionError(f"Provider resolution failed due to dependency errors: {unresolved_list}")
