from dependency.core.injection import ContainerInjection, ProviderInjection
from dependency.library.graph.models import Graph, Drawable, Cluster, Node, Edge

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
    graph.drawable[container.name] = cluster
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
