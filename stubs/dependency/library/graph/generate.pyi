from dependency.core import Registry as Registry
from dependency.core.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection
from dependency.library.graph.models import Cluster as Cluster, Edge as Edge, Graph as Graph, Node as Node

def generate_graph(output: str = 'build/output', ignore_modules: set[str] = {'BasePlugin'}) -> None:
    """Generate a graph visualization of the registered containers and providers.

    This method is intended for debugging and documentation purposes, allowing
    developers to visualize the structure of their dependency graph. It uses
    the graphviz library to create a visual representation of the nodes and
    their relationships.
    """
def process_container(graph: Graph, container: ContainerInjection, ignore_modules: set[str] = {'BasePlugin'}) -> Cluster: ...
def process_provider(graph: Graph, provider: ProviderInjection, ignore_modules: set[str] = {'BasePlugin'}) -> Node: ...
