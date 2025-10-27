from _typeshed import Incomplete
from dependency.core.agrupation.plugin import Plugin as Plugin
from dependency.core.injection.container import Container as Container
from dependency.core.injection.loader import InjectionLoader as InjectionLoader

class Entrypoint:
    """Entrypoint for the application.
    """
    loader: Incomplete
    def __init__(self, container: Container, plugins: list[Plugin]) -> None: ...
