from dependency.core.agrupation.plugin import Plugin as Plugin
from dependency.core.injection.injection import ProviderInjection as ProviderInjection
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.resolver import InjectionResolver as InjectionResolver
from dependency.core.resolution.strategy import ResolutionStrategy as ResolutionStrategy
from dependency.core.utils.threading import handle_exit as handle_exit
from typing import Iterable

class Entrypoint:
    """Entrypoint for the application.

    Attributes:
        init_time (float): Time when the entrypoint was initialized.
    """
    init_time: float
    modules: list[type[Plugin]]
    providers: list[ProviderInjection]
    strategy: ResolutionStrategy
    resolver: InjectionResolver
    def __init__(self, container: Container, plugins: Iterable[type[Plugin]], strategy: ResolutionStrategy | None = None) -> None: ...
    def initialize(self, extra: Iterable[ProviderInjection] = ()) -> None:
        """Initialize the application."""
    def shutdown(self) -> None:
        """Shut down every `Resource`-backed provider, in reverse resolution order.

        Applications used to have to do this themselves: the root `Container` cannot reach
        providers that live in plugin sub-containers, so `shutdown_resources()` reaches
        none of them (D-034, D-055).
        """
    @handle_exit
    def main_loop(self) -> None:
        """Main loop for the application. Waits indefinitely."""
