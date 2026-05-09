import logging
import time
from threading import Event
from typing import Iterable
from dependency.core.agrupation.plugin import Plugin
from dependency.core.injection.injection import ProviderInjection
from dependency.core.resolution.container import Container
from dependency.core.resolution.resolver import InjectionResolver
from dependency.core.resolution.strategy import ResolutionStrategy
from dependency.library.threading import handle_exit
_logger = logging.getLogger("dependency.loader")

class Entrypoint:
    """Entrypoint for the application.

    Attributes:
        init_time (float): Time when the entrypoint was initialized.
    """
    def __init__(self,
        container: Container,
        plugins: Iterable[type[Plugin]],
        strategy: ResolutionStrategy = ResolutionStrategy(),
    ) -> None:
        self.init_time: float = time.time()
        self.modules: list[type[Plugin]] = list(plugins)
        self.strategy: ResolutionStrategy = strategy

        self.resolver: InjectionResolver = InjectionResolver(container=container)

        if self.strategy.config.legacy_resolution:
            self.resolver.resolve_dependencies(
                modules=self.modules,
                strategy=self.strategy,
            )
        else:
            self.resolver.resolve_modules(modules=self.modules)

    def initialize(self,
        extra: Iterable[ProviderInjection] = (),
    ) -> None:
        """Initialize the application."""
        providers: set[ProviderInjection] = self.resolver.resolve_injectables(
            modules=self.modules,
            extra=extra,
        )
        self.resolver.resolve_providers(
            providers=providers,
            strategy=self.strategy,
        )
        _logger.info(f"Application initialized in {time.time() - self.init_time} seconds")

    @handle_exit
    def main_loop(self) -> None:
        """Main loop for the application. Waits indefinitely."""
        Event().wait() # pragma: no cover
