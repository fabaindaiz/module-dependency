import time
import logging
from dependency.core.agrupation.plugin import Plugin
from dependency.core.injection.container import Container
from dependency.core.injection.loader import InjectionLoader
_logger = logging.getLogger("DependencyLoader")
_init_time: float = time.time()

class Entrypoint:
    """Entrypoint for the application.
    """
    def __init__(self, container: Container, plugins: list[Plugin]) -> None:
        providers = [
            provider
            for plugin in plugins
            for provider in plugin.resolve_providers(container)]

        self.loader = InjectionLoader(
            container=container,
            providers=providers)
        self.loader.resolve_dependencies()
        _logger.info(f"Application started in {time.time() - _init_time} seconds")