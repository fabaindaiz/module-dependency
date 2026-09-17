from typing import Collection, Iterable
from dependency.core.injection import ContainerInjection, ProviderInjection
from dependency.core.injection.mixin import ContainerMixin
from dependency.library.graph.models import Graph, Cluster, Node, Edge

# A module-level constant, not a literal in the signature: a set literal in a default
# is built once and shared by every call, so one caller mutating it changes the default
# for every other caller in the process.
_DEFAULT_IGNORED: frozenset[str] = frozenset({"BasePlugin"})


def generate_graph(
    plugins: Iterable[type[ContainerMixin]],
    output: str = "build/output",
    ignore_modules: Collection[str] = _DEFAULT_IGNORED,
) -> None:
    """Generate a graph visualization of the dependency tree.

    Args:
        plugins: Root modules or plugins to include in the graph.
        output: The output path for the generated graph (rendered as SVG).
        ignore_modules: Module names to exclude from the graph.
    """
    graph: Graph = Graph(name="Dependency Graph")
    for plugin in plugins:
        graph.drawable.append(
            process_container(graph, plugin.injection, ignore_modules)
        )

    digraph = graph.draw()
    digraph.render(filename=output, format="svg")


def process_container(
    graph: Graph,
    container: ContainerInjection,
    ignore_modules: Collection[str] = _DEFAULT_IGNORED,
) -> Cluster:
    cluster = Cluster(name=container.name)
    for child in container.childs:
        if isinstance(child, ContainerInjection):
            cluster.childs.append(process_container(graph, child, ignore_modules))
        elif isinstance(child, ProviderInjection):
            cluster.childs.append(process_provider(graph, child, ignore_modules))
    return cluster


def process_provider(
    graph: Graph,
    provider: ProviderInjection,
    ignore_modules: Collection[str] = _DEFAULT_IGNORED,
) -> Node:
    if provider.parent is not None and str(provider.parent) in ignore_modules:
        return Node(name=provider.name)

    for dependent in provider.dependent:
        source: str = provider.injectable.interface_cls.__name__
        target: str = dependent.injectable.interface_cls.__name__
        edge: Edge = Edge(source=source, target=target)
        graph.edges.append(edge)

    in_degree: int = provider.weight()
    return Node(name=provider.name, in_degree=in_degree)
