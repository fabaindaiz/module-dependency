from dependency.core.agrupation.plugin import Plugin
from dependency.core.injection.container import Container
from dependency.core.injection.loader import InjectionLoader

class Entrypoint():
    def __init__(self, container: Container, plugins: list[type[Plugin]]) -> None:
        self.loader = InjectionLoader(container, plugins)
        self.loader.resolve_dependencies()