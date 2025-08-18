import logging
from dependency.core.injection.base import ProviderInjection, ProviderDependency
from dependency.core.exceptions import ResolutionError
logger = logging.getLogger("DependencyLoader")

def dep_in_resolved(provider: ProviderInjection, resolved: list[ProviderInjection]) -> bool:
    """Check if a provider is present in the resolved providers.

    Args:
        provider (ProviderInjection): The provider to check.
        resolved (list[ProviderInjection]): The resolved providers to check against.

    Returns:
        bool: True if the provider is resolved, False otherwise.
    """
    return any(
        issubclass(res.provided_cls, provider.interface_cls)
        for res in resolved
    )

def provider_is_resolved(dependency: ProviderDependency, resolved: list[ProviderInjection]) -> bool:
    """Check if all imports of a provider are in the resolved providers.

    Args:
        dependency (ProviderDependency): The provider dependency to check.
        resolved (list[ProviderInjection]): The resolved providers to check against.

    Returns:
        bool: True if all imports are resolved, False otherwise.
    """
    return all(
        dep_in_resolved(provider, resolved)
        for provider in dependency.imports
    )

def provider_unresolved(dependency: ProviderDependency, resolved: list[ProviderInjection]) -> list[ProviderInjection]:
    """Check if any imports of a provider are not in the resolved providers.

    Args:
        dependency (ProviderDependency): The provider dependency to check.
        resolved (list[ProviderInjection]): The resolved providers to check against.

    Returns:
        list[ProviderInjection]: A list of unresolved provider imports.
    """
    return [
        provider
        for provider in dependency.imports
        if not dep_in_resolved(provider, resolved)
    ]

class Cycle():
    """Represents a cycle in the dependency graph.
    """
    def __init__(self, elements: list[ProviderInjection]) -> None:
        self.elements = self.normalize(elements)
    
    @staticmethod
    def normalize(cycle: list[ProviderInjection]) -> tuple[str, ...]:
        # Rota el ciclo para que el menor (por str) esté primero, para comparar fácilmente
        min_idx = min(range(len(cycle)), key=lambda i: str(cycle[i]))
        normalized = cycle[min_idx:] + cycle[:min_idx] + [cycle[min_idx]]
        return tuple(str(p) for p in normalized)

    def __hash__(self) -> int:
        return hash(self.elements)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Cycle):
            return False
        return self.elements == other.elements

    def __repr__(self) -> str:
        return ' -> '.join(str(p) for p in self.elements)

def find_cycles(providers: list[ProviderInjection]) -> set[Cycle]:
    """Detect unique cycles in the dependency graph.

    Args:
        providers (list[ProviderInjection]): The list of provider injections to check for cycles.

    Returns:
        set[Cycle]: A set of cycles, each represented as a Cycle object.
    """
    cycles: set[Cycle] = set()

    def visit(node: ProviderInjection, path: list[ProviderInjection], visited: set[ProviderInjection]) -> None:
        if node in path:
            cycle_start = path.index(node)
            cycle = Cycle(path[cycle_start:])
            if cycle not in cycles:
                cycles.add(cycle)
            return
        if node in visited:
            return
        visited.add(node)
        for dep in node.imports:
            visit(dep, path + [node], visited)

    for provider in providers:
        visit(provider, [], set())
    return cycles

def raise_cycle_error(
        providers: list[ProviderInjection]
    ) -> None:
    """Raise an error if circular dependencies are detected.

    Args:
        providers (list[ProviderInjection]): The list of provider injections to check for cycles.

    Raises:
        ResolutionError: If circular dependencies are detected.
    """
    cycles = find_cycles(providers)
    if cycles:
        for cycle in cycles:
            logger.error(f"Circular import: {cycle}")
        raise ResolutionError("Circular dependencies detected")

def raise_dependency_error(
        dependencies: list[ProviderDependency],
        resolved: list[ProviderInjection],
    ) -> None:
    """Raise an error if unresolved dependencies are detected.

    Args:
        dependencies (list[ProviderDependency]): The list of provider dependencies to check.
        resolved (list[ProviderInjection]): The resolved providers to check against.

    Raises:
        ResolutionError: If unresolved dependencies are detected.
    """
    for dependency in dependencies:
        unresolved = provider_unresolved(dependency, resolved)
        logger.error(f"Provider {dependency} has unresolved dependencies: {unresolved}")
    raise ResolutionError("Providers cannot be resolved")

def raise_providers_error(
        providers: list[ProviderInjection],
        resolved: list[ProviderInjection],
    ) -> None:
    """Raise an error if unresolved provider imports are detected.

    Args:
        providers (list[ProviderInjection]): The list of provider injections to check.
        resolved (list[ProviderInjection]): The resolved providers to check against.
    """
    raise_cycle_error(providers)
    raise_dependency_error(
        dependencies=[
            provider.dependency
            for provider in providers],
        resolved=resolved
)