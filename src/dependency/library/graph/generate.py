from dependency.core import Registry
from dependency.core.injection import ContainerInjection, ProviderInjection
from dependency.library.graph.models import Graph, Cluster, Node, Edge

def generate_graph(
    output: str = "build/output",
    ignore_modules: set[str] = {"BasePlugin"},
) -> None:
    """Generate a graph visualization of the registered containers and providers.

    This method is intended for debugging and documentation purposes, allowing
    developers to visualize the structure of their dependency graph. It uses
    the graphviz library to create a visual representation of the nodes and
    their relationships.
    """

    graph: Graph = Graph(name="Dependency Graph")
    for container in Registry.containers:
        if container.is_root:
            graph.drawable.append(process_container(graph, container, ignore_modules))

    digraph = graph.draw()
    digraph.render(filename=output, format="svg") # type: ignore

def process_container(
    graph: Graph,
    container: ContainerInjection,
    ignore_modules: set[str] = {"BasePlugin"},
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
    ignore_modules: set[str] = {"BasePlugin"},
) -> Node:
    if provider.parent is not None and str(provider.parent) in ignore_modules:
        return Node(name=provider.name)

    for dependent in provider.injectable.dependent:
        source: str = provider.injectable.interface_cls.__name__
        target: str = dependent.interface_cls.__name__
        edge: Edge = Edge(source=source, target=target)
        graph.edges.append(edge)

    in_degree: int = provider.injectable.weight()
    return Node(name=provider.name, in_degree=in_degree)
