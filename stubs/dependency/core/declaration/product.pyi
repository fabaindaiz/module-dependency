from dependency.core.agrupation.module import Module as Module
from dependency.core.declaration.component import COMPONENT as COMPONENT, Component as Component, component as component
from dependency.core.injection.mixin import ProviderMixin as ProviderMixin
from dependency_injector import providers
from typing import Any, Callable, Iterable

class Product(Component):
    """Product Base Class
    """

def product(module: type[Module] | None = None, imports: Iterable[type[ProviderMixin]] = (), products: Iterable[type[ProviderMixin]] = (), provider: type[providers.Provider[Any]] = ..., partial_resolution: bool = False, bootstrap: bool = False) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
    """Decorator for Component class

    Args:
        module (type[Module], optional): Module where the component is registered. Defaults to None.
        imports (Iterable[type[ProviderMixin]], optional): List of components to be imported by the provider. Defaults to ().
        products (Iterable[type[ProviderMixin]], optional): List of products to be declared by the provider. Defaults to ().
        provider (providers.Provider[Any], optional): Provider to be used. Defaults to providers.Factory.
        partial_resolution (bool, optional): Whether the component should be resolved with partial resolution. Defaults to False.
        bootstrap (bool, optional): Whether the provider should be bootstrapped. Defaults to False.

    Raises:
        TypeError: If the wrapped class is not a subclass of Component.

    Returns:
        Callable[[type[COMPONENT]], COMPONENT]: Decorator function that wraps the product class.
    """
