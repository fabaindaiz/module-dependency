from dependency.core.exceptions import CancelInitialization as CancelInitialization, DeclarationError as DeclarationError, InitializationError as InitializationError
from dependency.core.utils.lazy import LazyList as LazyList
from dependency_injector import containers as containers, providers as providers
from typing import Any, Callable, Iterable

class Injectable:
    """Injectable Class representing a injectable dependency.
    """
    needs_full_resolution: bool
    component_cls: type
    modules_cls: set[type]
    provider_cls: providers.Provider[Any]
    is_resolved: bool
    def __init__(self, component_cls: type, modules_cls: set[type], provider: providers.Provider[Any], imports: Iterable['Injectable'] = (), products: Iterable['Injectable'] = (), bootstrap: Callable[[], Any] | None = None) -> None: ...
    @property
    def imports(self) -> list['Injectable']: ...
    @property
    def products(self) -> list['Injectable']: ...
    @property
    def import_resolved(self) -> bool: ...
    @property
    def provider(self) -> providers.Provider[Any]:
        """Return an instance from the provider."""
    def inject(self) -> Injectable:
        """Mark the injectable as resolved."""
    def wire(self, container: containers.DynamicContainer) -> None:
        """Wire the provider with the given container.

        Args:
            container (containers.DynamicContainer): Container to wire the provider with.
        """
    def init(self) -> None:
        """Execute the bootstrap function if it exists."""
