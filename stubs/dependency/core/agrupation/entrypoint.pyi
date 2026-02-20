from dependency.core.agrupation.plugin import Plugin as Plugin
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.resolver import InjectionResolver as InjectionResolver
from dependency.core.resolution.strategy import ResolutionStrategy as ResolutionStrategy
from typing import Iterable

class Entrypoint:
    """Entrypoint for the application.

    Attributes:
        init_time (float): Time when the entrypoint was initialized.
    """
    resolver: InjectionResolver
    def __init__(self, container: Container, plugins: Iterable[type[Plugin]], strategy: ResolutionStrategy = ...) -> None: ...
    def main_loop(self) -> None:
        """Main loop for the application. Waits indefinitely."""
