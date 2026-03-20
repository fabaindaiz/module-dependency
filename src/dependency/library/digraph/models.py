from abc import ABC, abstractmethod
from graphviz import Digraph
from pydantic import BaseModel

class Graph(BaseModel):
    name: str = "Dependency Graph"
    drawable: dict[str, Drawable] = {}
    edges: list[Edge] = []

    def draw(self) -> Digraph:
        graph: Digraph = Digraph(comment=self.name, engine="dot")
        graph.attr(rankdir="TB", newrank="true", ordering="in", overlap="false", splines="true", nodesep="1.0", ranksep="1.0")
        graph.attr("node", fontname="Helvetica", fontsize="12", margin="0.2", style="invis")

        for drawable in self.drawable.values():
            drawable.draw(graph)
        for edge in self.edges:
            edge.draw(graph)
        return graph

class Drawable(BaseModel, ABC):
    in_degree: int = 0
    name: str

    @abstractmethod
    def draw(self, parent: Digraph) -> None:
        pass

class Cluster(Drawable):
    childs: dict[str, Drawable] = {}
    include_modules: bool = True
    style: dict[str, str] = {
        "style": "rounded,filled",
        "fillcolor": "lightyellow",
        "color": "gray",
        "penwidth": "2",
    }

    def draw(self, parent: Digraph) -> None:
        name: str = f"cluster_{self.name}" if self.include_modules else self.name
        with parent.subgraph(name=name) as c:
            c.attr(label=self.name, **self.style)

            children: list[Drawable] = sorted(
                self.childs.values(),
                key=lambda c: c.in_degree
            )
            for child in children:
                child.draw(c)

            # Encadenar nodos verticalmente con aristas invisibles
            names = list(self.childs.keys())
            for i in range(len(names) - 1):
                c.edge(names[i], names[i+1], style="invis", weight="10")

class Node(Drawable):
    style: dict[str, str] = {
        "shape": "box",
        "style": "filled",
        "fillcolor": "white",
    }

    def draw(self, parent: Digraph) -> None:
        parent.node(self.name, **self.style)

class Edge(BaseModel):
    source: str
    target: str
    same_cluster: bool = False

    def draw(self, parent: Digraph) -> None:
        kwargs: dict[str, str] = {}
        if self.same_cluster:
            kwargs["constraint"] = "false"
        parent.edge(self.source, self.target, **kwargs)
