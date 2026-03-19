from dependency.core.agrupation.module import Module as Module
from dependency.core.declaration.component import COMPONENT as COMPONENT, Component as Component, component as component
from dependency.core.injection.mixin import ProviderMixin as ProviderMixin
from dependency_injector import providers
from typing import Any, Callable, Iterable

class Product(Component):
    """Base class for on-demand dependency units.

    A Product is semantically distinct from a Component in that it represents
    an object meant to be instantiated on demand (typically via providers.Factory),
    rather than a long-lived service. Products are usually created by factories or
    services as part of their operation, not consumed directly as injected services.

    Functionally, Product is equivalent to Component with provider=providers.Factory
    as the default. This class exists for semantic clarity and legacy compatibility.

    Products must be decorated with @product to be registered in the injection tree.
    """

def product(module: type[Module] | None = None, imports: Iterable[type[ProviderMixin]] = (), provider: type[providers.Provider[Any]] = ..., partial_resolution: bool = False, bootstrap: bool = False) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
    """Register a Product class into the injection tree.

    Convenience wrapper around @component that sets providers.Factory as the
    default provider, reflecting the semantic intent of Products as on-demand
    objects rather than long-lived services.

    Behaves identically to @component in all other respects. The decorated
    class must be a subclass of Component (typically also of Product for
    semantic clarity).

    Args:
        module (type[Module], optional): Module or Plugin this product belongs to.
            If None, the product is registered as an orphan. Defaults to None.
        imports (Iterable[type[ProviderMixin]], optional): Components this product
            depends on. Defaults to ().
        provider (type[providers.Provider], optional): Provider class to use.
            Defaults to providers.Factory.
        partial_resolution (bool, optional): If True, imports outside the current
            provider set are not required to be resolved. Defaults to False.
        bootstrap (bool, optional): If True, the provider is eagerly instantiated
            during the initialization phase. Defaults to False.

    Raises:
        TypeError: If the decorated class is not a subclass of Component.

    Returns:
        Callable[[type[COMPONENT]], type[COMPONENT]]: Decorator that registers the
            product class and returns it unchanged.
    """
