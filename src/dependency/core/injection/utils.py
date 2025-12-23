from typing import Any, Callable, Optional, Union
from dependency_injector import containers, providers
from dependency_injector.wiring import Modifier, Provide

class LazyProvide(Provide): # type: ignore
    """Lazy Provide Class for deferred provider resolution.
    """
    def __init__(self,
        provider: Callable[[], Union[providers.Provider[Any], containers.Container, str]],
        modifier: Optional[Modifier] = None,
    ) -> None:
        self._provider: Callable[[], Union[providers.Provider[Any], containers.Container, str]] = provider
        self.modifier: Optional[Modifier] = modifier

    @property
    def provider(self) -> Union[providers.Provider[Any], containers.Container, str]:
        return self._provider()
