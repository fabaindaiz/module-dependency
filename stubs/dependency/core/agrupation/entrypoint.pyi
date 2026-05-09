from dependency.core.agrupation.plugin import Plugin as Plugin
from dependency.core.injection.injection import ProviderInjection as ProviderInjection
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
    def __init__(self, container: Container, plugins: Iterable[type[Plugin]], strategy: ResolutionStrategy = ...) -> None: ...
    def initialize(self, extra: Iterable[ProviderInjection] = ()) -> None:
        """Initialize the application."""
    @handle_exit
    def main_loop(self) -> None:
        """Main loop for the application. Waits indefinitely."""
