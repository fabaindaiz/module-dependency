from dependency.core import Registry as Registry
from dependency.library.graph.models import Graph as Graph
from dependency.library.graph.process import process_container as process_container

def generate_graph(output: str = 'build/output', ignore_modules: set[str] = {'BasePlugin'}) -> None:
    """Generate a graph visualization of the registered containers and providers.

    This method is intended for debugging and documentation purposes, allowing
    developers to visualize the structure of their dependency graph. It uses
    the graphviz library to create a visual representation of the nodes and
    their relationships.
    """
