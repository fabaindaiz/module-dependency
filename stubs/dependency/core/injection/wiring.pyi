import abc
from abc import abstractmethod
from dependency_injector import containers as containers, providers as providers
from dependency_injector.wiring import Closing as Closing, Modifier as Modifier, Provide as Provide, _Marker
from typing import Any, Callable

TYPE_CHECKING: bool

class WiringMixin(metaclass=abc.ABCMeta):
    """Base class for wiring mixins."""
    @classmethod
    @abstractmethod
    def reference(cls) -> str:
        """Return the reference name of the Injectable."""

class LazyWiring(_Marker):
    """Base Lazy Class for deferred provider resolution.
    """
    modifier: Modifier | None
    def __init__(self, provider: type[WiringMixin] | Callable[[], providers.Provider[Any] | containers.Container | str], modifier: Modifier | None = None) -> None: ...
    @property
    def provider(self) -> providers.Provider[Any] | containers.Container | str:
        """Return the provider instance.

        Returns:
            The provider instance returned by the provider callable.
        """

LazyProvide: _Marker
LazyProvider: _Marker
LazyClosing: _Marker
