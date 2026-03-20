from dependency.core import Registry
from dependency.core.injection import ContainerInjection
from library.digraph.models import Graph
from library.digraph.process import process_container

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
    plugins: list[ContainerInjection] = [
        container for container in Registry.containers
        if container.is_root
    ]

    graph: Graph = Graph(name="Dependency Graph")
    graph.drawable = {
        plugin.name: process_container(graph, plugin, ignore_modules)
        for plugin in plugins
    }

    digraph = graph.draw()
    digraph.render(filename=output, format="svg")
