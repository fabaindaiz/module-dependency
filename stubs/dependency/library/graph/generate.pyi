from dependency.core.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection
from dependency.core.injection.mixin import ContainerMixin as ContainerMixin
from dependency.library.graph.models import Cluster as Cluster, Edge as Edge, Graph as Graph, Node as Node
from typing import Iterable

def generate_graph(plugins: Iterable[type[ContainerMixin]], output: str = 'build/output', ignore_modules: set[str] = {'BasePlugin'}) -> None:
    """Generate a graph visualization of the dependency tree.

    Args:
        plugins: Root modules or plugins to include in the graph.
        output: The output path for the generated graph (rendered as SVG).
        ignore_modules: Module names to exclude from the graph.
    """
def process_container(graph: Graph, container: ContainerInjection, ignore_modules: set[str] = {'BasePlugin'}) -> Cluster: ...
def process_provider(graph: Graph, provider: ProviderInjection, ignore_modules: set[str] = {'BasePlugin'}) -> Node: ...
