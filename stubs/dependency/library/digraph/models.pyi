import abc
from abc import ABC, abstractmethod
from graphviz import Digraph
from pydantic import BaseModel

class Graph(BaseModel):
    name: str
    drawable: dict[str, Drawable]
    edges: list[Edge]
    def draw(self) -> Digraph: ...

class Drawable(BaseModel, ABC, metaclass=abc.ABCMeta):
    in_degree: int
    name: str
    @abstractmethod
    def draw(self, parent: Digraph) -> None: ...

class Cluster(Drawable):
    childs: dict[str, Drawable]
    include_modules: bool
    style: dict[str, str]
    def draw(self, parent: Digraph) -> None: ...

class Node(Drawable):
    style: dict[str, str]
    def draw(self, parent: Digraph) -> None: ...

class Edge(BaseModel):
    source: str
    target: str
    same_cluster: bool
    def draw(self, parent: Digraph) -> None: ...
