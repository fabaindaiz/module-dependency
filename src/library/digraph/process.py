from dependency.core.injection import ContainerInjection, ProviderInjection
from library.digraph.models import Graph, Cluster, Node, Edge

def process_container(
    graph: Graph,
    container: ContainerInjection,
    ignore_modules: set[str] = {"BasePlugin"},
) -> Cluster:
    cluster = Cluster(name=container.name)
    for child in container.childs:
        if isinstance(child, ContainerInjection):
            cluster.childs[child.name] = process_container(graph, child, ignore_modules)
        elif isinstance(child, ProviderInjection):
            cluster.childs[child.name] = process_provider(graph, child, ignore_modules)
    return cluster

def process_provider(
    graph: Graph,
    provider: ProviderInjection,
    ignore_modules: set[str] = {"BasePlugin"},
) -> Node:
    if provider.parent is not None and str(provider.parent) in ignore_modules:
        return Node(name=provider.name)

    for imp in provider.injectable.dependent:
        src: str = provider.injectable.interface_cls.__name__
        dst: str = imp.interface_cls.__name__
        edge = Edge(source=src, target=dst)
        graph.edges.append(edge)

    in_degree = len(provider.injectable.imports) #- 2 * len(provider.injectable.dependent)
    return Node(name=provider.name, in_degree=in_degree)
