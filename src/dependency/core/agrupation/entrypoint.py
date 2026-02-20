import logging
import time
from threading import Event
from typing import Iterable
from dependency.core.agrupation.plugin import Plugin
from dependency.core.resolution.container import Container
from dependency.core.resolution.resolver import InjectionResolver
from dependency.core.resolution.strategy import ResolutionStrategy
_logger = logging.getLogger("dependency.loader")

class Entrypoint:
    """Entrypoint for the application.

    Attributes:
        init_time (float): Time when the entrypoint was initialized.
    """
    def __init__(self,
        container: Container,
        plugins: Iterable[type[Plugin]],
        strategy: ResolutionStrategy = ResolutionStrategy()
    ) -> None:
        init_time: float = time.time()

        self.resolver: InjectionResolver = InjectionResolver(
            container=container,
        )
        self.resolver.resolve_dependencies(
            modules=plugins,
            strategy=strategy,
        )
        _logger.info(f"Application started in {time.time() - init_time} seconds")

    def main_loop(self) -> None:
        """Main loop for the application. Waits indefinitely."""
        Event().wait() # pragma: no cover
