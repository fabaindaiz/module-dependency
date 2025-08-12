from _typeshed import Incomplete
from dependency.core.injection.base import ProviderDependency as ProviderDependency, ProviderInjection as ProviderInjection

logger: Incomplete

def dep_in_layers(provider: ProviderInjection, layers: list[list[ProviderInjection]]) -> bool:
    """Check if a provider is present in any of the resolved layers.

    Args:
        provider (ProviderInjection): The provider to check.
        layers (list[list[ProviderInjection]]): The resolved layers to check against.

    Returns:
        bool: True if the provider is in the layers, False otherwise.
    """
def provider_is_resolved(dependency: ProviderDependency, resolved_layers: list[list[ProviderInjection]]) -> bool:
    """Check if all imports of a provider are resolved in the given layers.

    Args:
        dependency (ProviderDependency): The provider dependency to check.
        resolved_layers (list[list[ProviderInjection]]): The resolved layers to check against.

    Returns:
        bool: True if all imports are resolved, False otherwise.
    """
def provider_unresolved(dependency: ProviderDependency, resolved_layers: list[list[ProviderInjection]]) -> list[ProviderInjection]:
    """Check if any imports of a provider are unresolved in the given layers.

    Args:
        dependency (ProviderDependency): The provider dependency to check.
        resolved_layers (list[list[ProviderInjection]]): The resolved layers to check against.

    Returns:
        list[ProviderInjection]: A list of unresolved provider imports.
    """

class Cycle:
    """Represents a cycle in the dependency graph.
    """
    elements: Incomplete
    def __init__(self, elements: list[ProviderInjection]) -> None: ...
    @staticmethod
    def normalize(cycle: list[ProviderInjection]) -> tuple[str, ...]: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other) -> bool: ...

def find_cycles(providers: list[ProviderInjection]) -> set[Cycle]:
    """Detect unique cycles in the dependency graph.

    Args:
        providers (list[ProviderInjection]): The list of provider injections to check for cycles.

    Returns:
        set[Cycle]: A set of cycles, each represented as a Cycle object.
    """
def raise_cycle_error(providers: list[ProviderInjection]) -> None: ...
def raise_dependency_error(dependencies: list[ProviderDependency], resolved_layers: list[list[ProviderInjection]]) -> None: ...
def raise_providers_error(providers: list[ProviderInjection], resolved_layers: list[list[ProviderInjection]]) -> None: ...
