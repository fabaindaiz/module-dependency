import abc
from abc import ABC, abstractmethod
from graphviz import Digraph
from pydantic import BaseModel

GROUP_SIZE: int

class Graph(BaseModel):
    name: str
    drawable: list[Drawable]
    edges: list[Edge]
    def draw(self) -> Digraph: ...

class Drawable(BaseModel, ABC, metaclass=abc.ABCMeta):
    name: str
    in_degree: int
    @abstractmethod
    def draw(self, parent: Digraph) -> None: ...

class Cluster(Drawable):
    childs: list[Drawable]
    style: dict[str, str]
    def draw(self, parent: Digraph) -> None: ...

class Node(Drawable):
    style: dict[str, str]
    def draw(self, parent: Digraph) -> None: ...

class Edge(BaseModel):
    source: str
    target: str
    def draw(self, parent: Digraph) -> None: ...
