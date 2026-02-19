from dependency.core.exceptions import CancelInitialization as CancelInitialization, DeclarationError as DeclarationError, InitializationError as InitializationError
from dependency_injector import containers as containers, providers
from enum import Enum as Enum
from typing import Any, Callable, Iterable

class Injectable:
    """Injectable Class represents a implementation of some kind that can be injected as a dependency.

    Attributes:
        interface_cls (T): The interface class that this injectable implements.

        imports (Iterable[Injectable]): List of injectables that this injectable depends on.
        products (Iterable[Injectable]): List of injectables that depend on this injectable.
    """
    interface_cls: type
    modules_cls: set[type]
    implementation: type | None
    imports: set['Injectable']
    dependent: set['Injectable']
    partial_resolution: bool
    force_resolution: bool
    is_resolved: bool
    def __init__(self, interface_cls: type) -> None: ...
    def check_resolved(self, providers: list['Injectable']) -> bool: ...
    def update_dependencies(self, imports: Iterable['Injectable'], partial_resolution: bool | None = None) -> None: ...
    def discard_dependencies(self, imports: Iterable['Injectable']) -> None: ...
    def add_implementation(self, implementation: type, modules_cls: Iterable[type], provider: providers.Provider[Any], bootstrap: Callable[[], Any] | None = None) -> None: ...
    @property
    def provider(self) -> providers.Provider[Any]:
        """Return the provider instance for this injectable."""
    @property
    def provide(self) -> providers.Provider[Any]:
        """Return the provide instance for this injectable."""
    def wire(self, container: containers.DynamicContainer) -> None:
        """Wire the provider with the given container.

        Args:
            container (containers.DynamicContainer): Container to wire the provider with.
        """
    def init(self) -> None:
        """Execute the bootstrap function if it exists."""
    def __hash__(self) -> int: ...
