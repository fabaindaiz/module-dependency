from dependency.core.exceptions import ResolutionError as ResolutionError
from dependency.core.injection.injectable import Injectable as Injectable

class Cycle:
    """Represents a cycle in the dependency graph.
    """
    elements: tuple[str, ...]
    def __init__(self, elements: list[Injectable]) -> None: ...
    @staticmethod
    def normalize(cycle: list[Injectable]) -> tuple[str, ...]: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...

def find_cycles(injectables: list[Injectable]) -> set[Cycle]:
    """Detect unique cycles in the dependency graph.

    Args:
        injectables (list[Injectable]): The list of provider injections to check for cycles.

    Returns:
        set[Cycle]: A set of cycles, each represented as a Cycle object.
    """
def raise_cycle_error(injectables: list[Injectable]) -> None:
    """Raise an error if circular dependencies are detected.

    Args:
        providers (list[ProviderInjection]): The list of provider injections to check for cycles.

    Raises:
        ResolutionError: If circular dependencies are detected.
    """
def raise_dependency_error(unresolved_injectable: list[Injectable]) -> None:
    """Raise an error if unresolved dependencies are detected.

    Args:
        dependencies (list[ProviderDependency]): The list of provider dependencies to check.
        resolved (list[ProviderInjection]): The resolved providers to check against.

    Raises:
        ResolutionError: If unresolved dependencies are detected.
    """
def raise_providers_error(injectables: list[Injectable], unresolved: list[Injectable]) -> None:
    """Raise an error if unresolved provider imports are detected.

    Args:
        providers (list[ProviderInjection]): The list of provider injections to check.
        unresolved (list[ProviderInjection]): The resolved providers to check against.

    Raises:
        ResolutionError: If unresolved dependencies or cycles are detected.
    """
