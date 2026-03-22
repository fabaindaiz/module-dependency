from dependency.core import Registry
from dependency.core.injection import ContainerInjection, ProviderInjection
from dependency.library.graph.models import Graph, Cluster, Node, Edge

def generate_graph(
    output: str = "build/output",
    ignore_modules: set[str] = {"BasePlugin"},
) -> None:
    """Generate a graph visualization of the registered containers and providers.

    This method allows you to visualize the structure of your dependency graph, including the
    containers (modules) and providers (components/products) and their relationships. The generated
    graph can be used for debugging, documentation, or simply to understand the structure of your
    dependency graph. The output will be saved as an SVG file at the specified location.

    Args:
        output: The output path for the generated graph.
        ignore_modules: A set of module names to ignore during graph generation.
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
