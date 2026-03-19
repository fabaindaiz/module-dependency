from dependency.core.utils.cycle import find_cycles

class FakeInjectable:
    """Injectable mínimo para testear find_cycles sin dependencias del framework."""
    def __init__(self, name: str) -> None:
        self.name = name
        self.imports: list['FakeInjectable'] = []

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FakeInjectable) and self.name == other.name


def test_cycle_simple() -> None:
    """Ciclo directo: a -> b -> a."""
    a = FakeInjectable("a")
    b = FakeInjectable("b")
    a.imports = [b]
    b.imports = [a]

    cycles = find_cycles(lambda i: i.imports, [a])
    assert len(cycles) == 1

def test_no_cycles() -> None:
    """Grafo sin ciclos no reporta nada."""
    a = FakeInjectable("a")
    b = FakeInjectable("b")
    c = FakeInjectable("c")
    a.imports = [b, c]

    cycles = find_cycles(lambda i: i.imports, [a])
    assert len(cycles) == 0

def test_cycle_two_paths_same_root() -> None:
    """Dos caminos desde la misma raíz hacia el mismo ciclo.

    Grafo:
        a -> b -> a  (ciclo directo)
        a -> c -> b  (segundo camino que llega a b)

    Con el root único a, el DFS original marca b como visited al
    explorar la primera rama (a->b->a), y luego cuando explora
    a->c->b, omite b por estar en visited — perdiendo el ciclo
    a->c->b->a. El resultado correcto son dos ciclos distintos,
    independientemente del orden de iteración.
    """
    a = FakeInjectable("a")
    b = FakeInjectable("b")
    c = FakeInjectable("c")
    a.imports = [b, c]
    b.imports = [a]
    c.imports = [b]

    cycles = find_cycles(lambda i: i.imports, [a])

    cycle_nodes = {node for cycle in cycles for node in cycle.elements}
    assert len(cycles) == 2, f"Se esperaban 2 ciclos (a->b->a y a->c->b->a), se encontraron: {cycles}"
    assert a in cycle_nodes
    assert b in cycle_nodes
    assert c in cycle_nodes
