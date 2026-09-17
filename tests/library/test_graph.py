"""Coverage for dependency.library.graph, which previously had none.

That gap is why a NameError from an unquoted forward reference shipped and broke the
module on every supported Python except 3.14 (D-017). These tests import it, which is
the part that was missing.
"""
import shutil
from pathlib import Path
import pytest
from dependency.core import (
    Component,
    Container,
    Entrypoint,
    Plugin,
    PluginMeta,
    component,
    instance,
    module,
    providers,
)
from dependency.core.injection import ContainerInjection, ProviderInjection
from dependency.library.graph import generate_graph
from dependency.library.graph.generate import process_container, process_provider
from dependency.library.graph.models import Cluster, Edge, Graph, Node


@module()
class GraphPlugin(Plugin):
    meta = PluginMeta(name="graph_plugin", version="0.1.0")


@module(module=GraphPlugin)
class GraphChildModule(Plugin):
    meta = PluginMeta(name="graph_child", version="0.1.0")


@component(module=GraphPlugin)
class GraphLeaf(Component):
    def run(self) -> str: ...


@instance(provider=providers.Singleton)
class GraphLeafImpl(GraphLeaf):
    def run(self) -> str:
        return "leaf"


@component(module=GraphChildModule, imports=[GraphLeaf])
class GraphRoot(Component):
    def run(self) -> str: ...


@instance(provider=providers.Singleton)
class GraphRootImpl(GraphRoot):
    def run(self) -> str:
        return "root"


@pytest.fixture(scope="module", autouse=True)
def resolved_app() -> None:
    class App(Entrypoint):
        def __init__(self) -> None:
            super().__init__(Container.from_dict({"config": True}), [GraphPlugin])
            super().initialize()

    App()


# ── models ───────────────────────────────────────────────────────────────────

def test_node_renders_into_a_digraph() -> None:
    graph = Graph(name="test", drawable=[Node(name="Solo")])
    rendered = graph.draw().source
    assert "Solo" in rendered


def test_cluster_wraps_its_children() -> None:
    cluster = Cluster(name="Group", childs=[Node(name="Inner")])
    rendered = Graph(name="test", drawable=[cluster]).draw().source
    assert "cluster_Group" in rendered
    assert "Inner" in rendered


def test_edges_are_drawn_between_nodes() -> None:
    graph = Graph(
        name="test",
        drawable=[Node(name="A"), Node(name="B")],
        edges=[Edge(source="A", target="B")],
    )
    rendered = graph.draw().source
    assert "A -> B" in rendered


def test_graph_instances_do_not_share_their_lists() -> None:
    """The bug class that broke this module: mutable state leaking between models."""
    first = Graph(name="one")
    second = Graph(name="two")
    first.drawable.append(Node(name="OnlyInFirst"))
    assert second.drawable == []


def test_cluster_orders_children_by_in_degree() -> None:
    cluster = Cluster(
        name="Ordered",
        childs=[Node(name="Deep", in_degree=9), Node(name="Shallow", in_degree=0)],
    )
    rendered = Graph(name="test", drawable=[cluster]).draw().source
    assert rendered.index("Shallow") < rendered.index("Deep")


# ── walking a real injection tree ────────────────────────────────────────────

def test_process_provider_reports_weight_as_in_degree() -> None:
    graph = Graph(name="test")
    node = process_provider(graph, GraphRoot.injection, ignore_modules=set())
    assert isinstance(node, Node)
    assert node.name == "GraphRoot"
    assert node.in_degree == GraphRoot.injection.weight()


def test_process_provider_records_an_edge_per_dependent() -> None:
    graph = Graph(name="test")
    process_provider(graph, GraphLeaf.injection, ignore_modules=set())
    assert Edge(source="GraphLeaf", target="GraphRoot") in graph.edges


def test_process_provider_skips_ignored_modules() -> None:
    graph = Graph(name="test")
    node = process_provider(graph, GraphRoot.injection, ignore_modules={"GraphChildModule"})
    assert node.in_degree == 0
    assert graph.edges == []


def test_process_container_recurses_into_child_containers() -> None:
    graph = Graph(name="test")
    cluster = process_container(graph, GraphPlugin.injection, ignore_modules=set())
    assert cluster.name == "GraphPlugin"
    names = {child.name for child in cluster.childs}
    assert "GraphLeaf" in names
    assert "GraphChildModule" in names


def test_process_container_handles_both_node_kinds() -> None:
    graph = Graph(name="test")
    cluster = process_container(graph, GraphPlugin.injection, ignore_modules=set())
    kinds = {type(child).__name__ for child in cluster.childs}
    assert kinds == {"Cluster", "Node"}
    assert isinstance(GraphPlugin.injection, ContainerInjection)
    assert isinstance(GraphLeaf.injection, ProviderInjection)


# ── the public entry point ───────────────────────────────────────────────────

@pytest.mark.skipif(
    shutil.which("dot") is None,
    reason="rendering needs the graphviz 'dot' binary, which pip install graphviz does "
    "not provide; the Python package alone is enough for every other test here",
)
def test_generate_graph_writes_an_svg(tmp_path: Path) -> None:
    output = tmp_path / "graph"
    generate_graph([GraphPlugin], output=str(output), ignore_modules=set())

    svg = output.with_suffix(".svg")
    assert svg.exists(), "generate_graph must render an SVG at <output>.svg"

    content = svg.read_text()
    assert "GraphLeaf" in content
    assert "GraphRoot" in content
