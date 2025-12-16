import logging
from dependency.core.injection.injectable import Injectable
from dependency.core.exceptions import ResolutionError
logger = logging.getLogger("DependencyLoader")

class Cycle:
    """Represents a cycle in the dependency graph.
    """
    def __init__(self, elements: list[Injectable]) -> None:
        self.elements: tuple[str, ...] = self.normalize(elements)

    @staticmethod
    def normalize(cycle: list[Injectable]) -> tuple[str, ...]:
        # Rota el ciclo para que el menor (por str) esté primero, para comparar fácilmente
        min_idx = min(range(len(cycle)), key=lambda i: str(cycle[i]))
        normalized = cycle[min_idx:] + cycle[:min_idx] + [cycle[min_idx]]
        return tuple(str(p) for p in normalized)

    def __hash__(self) -> int:
        return hash(self.elements)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cycle):
            return False
        return self.elements == other.elements

    def __repr__(self) -> str:
        return ' -> '.join(str(p) for p in self.elements)

def find_cycles(injectables: list[Injectable]) -> set[Cycle]:
    """Detect unique cycles in the dependency graph.

    Args:
        injectables (list[Injectable]): The list of provider injections to check for cycles.

    Returns:
        set[Cycle]: A set of cycles, each represented as a Cycle object.
    """
    cycles: set[Cycle] = set()

    def visit(node: Injectable, path: list[Injectable], visited: set[Injectable]) -> None:
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

    for injectable in injectables:
        visit(injectable, [], set())
    return cycles

def raise_cycle_error(
    injectables: list[Injectable]
) -> None:
    """Raise an error if circular dependencies are detected.

    Args:
        providers (list[ProviderInjection]): The list of provider injections to check for cycles.

    Raises:
        ResolutionError: If circular dependencies are detected.
    """
    cycles = find_cycles(injectables)
    if cycles:
        for cycle in cycles:
            logger.error(f"Circular import: {cycle}")
        raise ResolutionError("Circular dependencies detected")

def raise_dependency_error(
    unresolved_injectable: list[Injectable],
) -> None:
    """Raise an error if unresolved dependencies are detected.

    Args:
        dependencies (list[ProviderDependency]): The list of provider dependencies to check.
        resolved (list[ProviderInjection]): The resolved providers to check against.

    Raises:
        ResolutionError: If unresolved dependencies are detected.
    """
    for injectable in unresolved_injectable:
        unresolved = [
            dependency
            for dependency in injectable.imports
            if not dependency.is_resolved
        ]
        logger.error(f"Provider {injectable} has unresolved dependencies: {unresolved}")
    raise ResolutionError("Providers cannot be resolved")

# TODO: Allow to raise both errors together with extended information
def raise_providers_error(
    injectables: list[Injectable],
    unresolved: list[Injectable],
) -> None:
    """Raise an error if unresolved provider imports are detected.

    Args:
        providers (list[ProviderInjection]): The list of provider injections to check.
        unresolved (list[ProviderInjection]): The resolved providers to check against.

    Raises:
        ResolutionError: If unresolved dependencies or cycles are detected.
    """
    raise_cycle_error(injectables)
    raise_dependency_error(unresolved)
