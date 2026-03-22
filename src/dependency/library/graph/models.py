from abc import ABC, abstractmethod
from itertools import groupby, pairwise
from graphviz import Digraph
from pydantic import BaseModel

GROUP_SIZE: int = 2

class Graph(BaseModel):
    name: str = "Dependency Graph"
    drawable: list[Drawable] = []
    edges: list[Edge] = []

    def draw(self) -> Digraph:
        graph: Digraph = Digraph(comment=self.name, engine="dot")
        graph.attr(rankdir="TB", newrank="true", ordering="in", overlap="false", splines="true", nodesep="1.0", ranksep="1.0")
        graph.attr("node", fontname="Helvetica", fontsize="12", margin="0.2", style="invis")

        for drawable in self.drawable:
            drawable.draw(graph)
        for edge in self.edges:
            edge.draw(graph)
        return graph

class Drawable(BaseModel, ABC):
    name: str
    in_degree: int = 0

    @abstractmethod
    def draw(self, parent: Digraph) -> None:
        pass

class Cluster(Drawable):
    childs: list[Drawable] = []
    style: dict[str, str] = {
        "style": "rounded,filled",
        "fillcolor": "lightyellow",
        "color": "gray",
        "penwidth": "2",
    }

    def draw(self, parent: Digraph) -> None:
        with parent.subgraph(name=f"cluster_{self.name}") as c:
            c.attr(label=self.name, **self.style)

            # Agrupar por profundidad y ordenar por in_degree dentro de cada grupo
            def bucket(x: Drawable): return x.in_degree // GROUP_SIZE
            childs: list[Drawable] = sorted(self.childs, key=lambda c: c.in_degree)
            groups = [list(g) for _, g in groupby(childs, key=bucket)]

            for group in groups:
                for child in group:
                    child.draw(c)

                # Arista invisible entre nodos del mismo grupo para mantenerlos juntos
                for i, (n1, n2) in enumerate(pairwise(group)):
                    if isinstance(n2, Node) and i % min(2,  max(1, len(group) // GROUP_SIZE)) != 0:
                        c.edge(n1.name, n2.name, style="invis", weight="1")

            # Arista invisible solo entre representantes de grupos consecutivos
            for (g1, g2) in pairwise(groups):
                c.edge(g1[0].name, g2[0].name, style="invis", weight="1")

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

    def draw(self, parent: Digraph) -> None:
        kwargs: dict[str, str] = {}
        parent.edge(self.source, self.target, weight="5", minlen="1", **kwargs)
