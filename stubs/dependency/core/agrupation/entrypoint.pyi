from _typeshed import Incomplete
from dependency.core.agrupation.plugin import Plugin
from dependency.core.injection.container import Container as Container

logger: Incomplete
init_time: Incomplete

class Entrypoint:
    """Entrypoint for the application.
    """
    loader: Incomplete
    def __init__(self, container: Container, plugins: list[type[Plugin]]) -> None: ...
