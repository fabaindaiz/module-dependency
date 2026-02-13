from dependency.core.exceptions import CancelInitialization as CancelInitialization, DeclarationError as DeclarationError, InitializationError as InitializationError
from dependency_injector import containers as containers, providers as providers
from typing import Any, Callable, Iterable, Self

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
    partial_resolution: bool
    is_resolved: bool
    def __init__(self, interface_cls: type) -> None: ...
    @property
    def imports(self) -> Iterable['Injectable']:
        """Return the set of imports for this provider injection."""
    @property
    def products(self) -> Iterable['Injectable']:
        """Return the set of products for this provider injection."""
    @property
    def import_resolved(self) -> bool: ...
    def as_import(self, provider: Injectable) -> Self: ...
    def as_product(self, provider: Injectable) -> Self: ...
    def add_dependencies(self, imports: Iterable['Injectable'], products: Iterable['Injectable'], partial_resolution: bool = False) -> None: ...
    def add_implementation(self, implementation: type, modules_cls: Iterable[type], provider: providers.Provider[Any], bootstrap: Callable[[], Any] | None = None) -> None: ...
    @property
    def injection(self) -> providers.Provider[Any]:
        """Return an instance from the provider."""
    @property
    def provider(self) -> providers.Provider[Any]:
        """Return the provider instance for this injectable."""
    def inject(self) -> Self:
        """Mark the provider injection as resolved."""
    def wire(self, container: containers.DynamicContainer) -> None:
        """Wire the provider with the given container.

        Args:
            container (containers.DynamicContainer): Container to wire the provider with.
        """
    def init(self) -> None:
        """Execute the bootstrap function if it exists."""
