from dependency.core.agrupation.fallback import initialize_fallback as initialize_fallback
from dependency.core.agrupation.plugin import Plugin as Plugin
from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.resolver import InjectionResolver as InjectionResolver
from dependency.core.resolution.strategy import ResolutionStrategy as ResolutionStrategy
from dependency.library.threading import handle_exit as handle_exit
from typing import Iterable

class Entrypoint:
    """Entrypoint for the application.

    Attributes:
        init_time (float): Time when the entrypoint was initialized.
    """
    init_time: float
    modules: list[type[Plugin]]
    strategy: ResolutionStrategy
    resolver: InjectionResolver
    def __init__(self, container: Container, plugins: Iterable[type[Plugin]], strategy: ResolutionStrategy = ...) -> None:
        """Set up the application entrypoint.

        Stores the plugin list and initializes the InjectionResolver with the
        given container. Resolves the structural dependency tree so that the
        injection hierarchy is ready before instance imports loaded.
        Full resolution is deferred to initialize().

        Args:
            container (Container): The application container holding configuration.
            plugins (Iterable[type[Plugin]]): List of root Plugin classes to load.
            strategy (ResolutionStrategy): Resolution strategy to use. Defaults to
                a standard ResolutionStrategy with default config.
        """
    def initialize(self, injectables: Iterable[Injectable] = ()) -> None:
        """Initialize the application."""
    @handle_exit
    def main_loop(self) -> None:
        """Main loop for the application. Waits indefinitely.

        This method is intended to be called after the application has been initialized.
        """
