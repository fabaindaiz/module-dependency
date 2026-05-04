from dependency.core import Registry as Registry
from dependency.core.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection
from dependency.library.graph.models import Cluster as Cluster, Edge as Edge, Graph as Graph, Node as Node

def generate_graph(output: str = 'build/output', ignore_modules: set[str] = {'BasePlugin'}) -> None:
    """Generate a graph visualization of the registered containers and providers.

    This method allows you to visualize the structure of your dependency graph, including the
    containers (modules) and providers (components/products) and their relationships. The generated
    graph can be used for debugging, documentation, or simply to understand the structure of your
    dependency graph. The output will be saved as an SVG file at the specified location.

    Args:
        output: The output path for the generated graph.
        ignore_modules: A set of module names to ignore during graph generation.
    """
def process_container(graph: Graph, container: ContainerInjection, ignore_modules: set[str] = {'BasePlugin'}) -> Cluster: ...
def process_provider(graph: Graph, provider: ProviderInjection, ignore_modules: set[str] = {'BasePlugin'}) -> Node: ...
