from abc import abstractmethod
from typing import Any, Callable, Optional, Union
from dependency_injector import containers, providers
from dependency_injector.wiring import _Marker, Modifier, Provide, Provider, Closing

# Constant that's True when type checking, but False here.
TYPE_CHECKING = False

class WiringMixin:
    """Base class for wiring mixins."""
    @classmethod
    @abstractmethod
    def reference(cls) -> str:
        """Return the reference name of the Injectable."""

class LazyWiring(_Marker):
    """Base Lazy Class for deferred provider resolution.
    """
    def __init__(self,
        provider: Union[type[WiringMixin], Callable[[], Union[providers.Provider[Any], containers.Container, str]]],
        modifier: Optional[Modifier] = None,
    ) -> None:
        if isinstance(provider, type) and issubclass(provider, WiringMixin):
            provider = provider.reference
        self._provider: Callable[[], Union[providers.Provider[Any], containers.Container, str]] = provider # type: ignore
        self.modifier: Optional[Modifier] = modifier

    @property
    def provider(self) -> Union[providers.Provider[Any], containers.Container, str]:
        """Return the provider instance.

        Returns:
            The provider instance returned by the provider callable.
        """
        return self._provider()

if TYPE_CHECKING:  # noqa#

    LazyProvide: _Marker
    LazyProvider: _Marker
    LazyClosing: _Marker
else:

    class LazyProvide(LazyWiring, Provide): # type: ignore
        """Lazy Provide Class for deferred provider resolution.
        """

    class LazyProvider(LazyWiring, Provider): # type: ignore
        """Lazy Provider Class for deferred provider resolution.
        """

    class LazyClosing(LazyWiring, Closing): # type: ignore
        """Lazy Closing Class for deferred provider resolution.
        """
