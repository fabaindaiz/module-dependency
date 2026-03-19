from graphviz import Digraph
from pprint import pformat
from dependency.core import Registry
from dependency.core.injection import Injectable, ProviderInjection

IGNORE_MODULES = {"BasePlugin"}

def generate_graph(output: str = "build/output", include_modules: bool = False) -> None:
    """Generate a graph visualization of the registered containers and providers.

    This method is intended for debugging and documentation purposes, allowing
    developers to visualize the structure of their dependency graph. It uses
    the graphviz library to create a visual representation of the nodes and
    their relationships.

    The generated graph can be saved to a file or displayed directly, depending
    on the implementation details of the graph generation logic.
    """
    injectable_to_provider: dict[Injectable, ProviderInjection] = {
        provider.injectable: provider
        for provider in Registry.providers
    }

    def find_first_parent(provider: ProviderInjection, visited: set[ProviderInjection] | None = None) -> str:
        if visited is None:
            visited = set()
        if provider in visited:
            return "fallback"
        visited.add(provider)

        if provider.parent is not None:
            if provider.parent.name not in ("RootInternal", "FallbackInternal"):
                return provider.parent.name

        scores: dict[str, int] = {}
        for dependent in provider.injectable.dependent:
            dep_provider = injectable_to_provider.get(dependent)
            if dep_provider is None:
                continue
            result = find_first_parent(dep_provider, visited)
            if result != "fallback":
                scores[result] = scores.get(result, 0) + 1

        if scores:
            return max(scores, key=lambda k: scores[k])
        return "fallback"

    module_structure: dict[str, list[str]] = {}
    for provider in Registry.providers:
        name: str = provider.injectable.interface_cls.__name__
        if provider.parent is not None:
            module_structure.setdefault(find_first_parent(provider), []).append(name)
        else:
            module_structure.setdefault("fallback", []).append(name)
    print(f"Module structure for graph generation:\n{pformat(module_structure)}")

    graph = Digraph(comment="Dependency Graph", engine="dot")
    graph.attr(rankdir="TB", splines="true", nodesep="0.8", ranksep="0.8", ordering="out", concentrate="true")
    graph.attr("node", fontname="Helvetica", fontsize="11")

    for module, providers in module_structure.items():
        module_name = f"cluster_{module}" if include_modules else module
        with graph.subgraph(name=module_name) as c:
            c.attr(label=module, style="rounded,filled", fillcolor="lightyellow", color="gray")
            for node in providers:
                c.node(node, shape="box", style="filled", fillcolor="white")

    for provider in Registry.providers:
        for imp in provider.injectable.imports:
            src_provider: ProviderInjection|None = injectable_to_provider.get(imp)
            if src_provider is not None and str(src_provider.parent) in IGNORE_MODULES:
                continue

            src = imp.interface_cls.__name__
            dst = provider.injectable.interface_cls.__name__

            # Determinar si la arista cruza clusters
            same_cluster = (
                src_provider is not None and
                src_provider.parent == provider.parent
            )
            if same_cluster:
                graph.edge(src, dst)  # arista interna, influye en layout
            else:
                graph.edge(src, dst)#, constraint="false")  # externa, solo visual

    graph.render(filename=output, format="svg")
