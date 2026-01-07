from typing import Any, Callable, Generic, Iterable, Optional, TypeVar, Union
from dependency_injector import containers, providers
from dependency_injector.wiring import Modifier, Provide, Provider, Closing

T = TypeVar('T')

class LazyList(Generic[T]):
    """Lazy List Class for deferred list evaluation.
    """
    def __init__(self, iterable: Iterable[T]) -> None:
        super().__init__()
        self._iterable = iterable
        self._list: Optional[list[T]] = None

    def __call__(self, *args: Any, **kwargs: Any) -> list[T]:
        if self._list is None:
            self._list = list(self._iterable)
        return self._list

class LazyWiring:
    """Base Lazy Class for deferred provider resolution.
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

class LazyProvide(LazyWiring, Provide): # type: ignore
    """Lazy Provide Class for deferred provider resolution.
    """
    pass

class LazyProvider(LazyWiring, Provider): # type: ignore
    """Lazy Provider Class for deferred provider resolution.
    """
    pass

class LazyClosing(LazyWiring, Closing): # type: ignore
    """Lazy Closing Class for deferred provider resolution.
    """
    pass
