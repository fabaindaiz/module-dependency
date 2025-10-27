from dependency.core.exceptions import DependencyError as DependencyError
from dependency.core.injection.base import ProviderDependency as ProviderDependency, ProviderInjection as ProviderInjection

def dep_in_resolved(provider: ProviderInjection, resolved: list[ProviderInjection]) -> bool:
    """Check if a provider is present in the resolved providers.

    Args:
        provider (ProviderInjection): The provider to check.
        resolved (list[ProviderInjection]): The resolved providers to check against.

    Returns:
        bool: True if the provider is resolved, False otherwise.
    """
def provider_is_resolved(dependency: ProviderDependency, resolved: list[ProviderInjection]) -> bool:
    """Check if all imports of a provider are in the resolved providers.

    Args:
        dependency (ProviderDependency): The provider dependency to check.
        resolved (list[ProviderInjection]): The resolved providers to check against.

    Returns:
        bool: True if all imports are resolved, False otherwise.
    """
def provider_unresolved(dependency: ProviderDependency, resolved: list[ProviderInjection]) -> list[ProviderInjection]:
    """Check if any imports of a provider are not in the resolved providers.

    Args:
        dependency (ProviderDependency): The provider dependency to check.
        resolved (list[ProviderInjection]): The resolved providers to check against.

    Returns:
        list[ProviderInjection]: A list of unresolved provider imports.
    """

class Cycle:
    """Represents a cycle in the dependency graph.
    """
    elements: tuple[str, ...]
    def __init__(self, elements: list[ProviderInjection]) -> None: ...
    @staticmethod
    def normalize(cycle: list[ProviderInjection]) -> tuple[str, ...]: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...

def find_cycles(providers: list[ProviderInjection]) -> set[Cycle]:
    """Detect unique cycles in the dependency graph.

    Args:
        providers (list[ProviderInjection]): The list of provider injections to check for cycles.

    Returns:
        set[Cycle]: A set of cycles, each represented as a Cycle object.
    """
def raise_cycle_error(providers: list[ProviderInjection]) -> None: ...
def raise_dependency_error(dependencies: list[ProviderDependency], resolved: list[ProviderInjection]) -> None: ...
def raise_providers_error(providers: list[ProviderInjection], resolved: list[ProviderInjection]) -> None: ...
