from dependency_injector import containers as containers, providers as providers
from dependency_injector.wiring import Modifier as Modifier, Provide
from typing import Any, Callable

class LazyProvide(Provide):
    """Lazy Provide Class for deferred provider resolution.
    """
    modifier: Modifier | None
    def __init__(self, provider: Callable[[], providers.Provider[Any] | containers.Container | str], modifier: Modifier | None = None) -> None: ...
    @property
    def provider(self) -> providers.Provider[Any] | containers.Container | str: ...
