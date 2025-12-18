from dependency.core.exceptions import CancelInitError as CancelInitError
from dependency_injector import containers as containers, providers
from typing import Any, Callable

class Injectable:
    """Injectable Class representing a injectable dependency.
    """
    component_cls: type
    provided_cls: type
    provider_cls: type[providers.Provider[Any]]
    modules_cls: set[type]
    imports: list['Injectable']
    products: list['Injectable']
    bootstrap: Callable[[], Any] | None
    is_resolved: bool
    def __init__(self, component_cls: type, provided_cls: type, provider_cls: type[providers.Provider[Any]] = ..., imports: list['Injectable'] = [], products: list['Injectable'] = [], bootstrap: Callable[[], Any] | None = None) -> None: ...
    @property
    def import_resolved(self) -> bool: ...
    @property
    def provider(self) -> providers.Provider[Any]:
        """Return an instance from the provider."""
    def do_wiring(self, container: containers.DynamicContainer) -> Injectable:
        """Wire the provider with the given container."""
    def do_bootstrap(self) -> None:
        """Execute the bootstrap function if it exists."""
