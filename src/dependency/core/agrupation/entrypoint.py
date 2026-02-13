import logging
import time
from threading import Event
from typing import Iterable
from dependency.core.agrupation.plugin import Plugin
from dependency.core.injection.injectable import Injectable
from dependency.core.resolution.container import Container
from dependency.core.resolution.resolver import InjectionResolver
_logger = logging.getLogger("dependency.loader")

class Entrypoint:
    """Entrypoint for the application.

    Attributes:
        init_time (float): Time when the entrypoint was initialized.
    """
    init_time: float = time.time()

    def __init__(self,
        container: Container,
        plugins: Iterable[type[Plugin]]
    ) -> None:
        providers: list[Injectable] = []

        for plugin in plugins:
            plugin.resolve_container(container=container)
            providers.extend(plugin.resolve_providers())

        self.resolver: InjectionResolver = InjectionResolver(
            container=container,
            providers=providers
        )

        self.resolver.resolve_dependencies()
        _logger.info(f"Application started in {time.time() - self.init_time} seconds")

    def main_loop(self) -> None:
        """Main loop for the application. Waits indefinitely."""
        Event().wait() # pragma: no cover
