from dependency.core.agrupation.module import Module as Module
from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.injection import ProviderInjection as ProviderInjection
from dependency.core.injection.mixin import ProviderMixin as ProviderMixin
from dependency_injector import providers
from typing import Any, Callable, Iterable, TypeVar

PRODUCT = TypeVar('PRODUCT', bound='Product')

class Product(ProviderMixin):
    """Product Base Class
    """
    implicit_component: type[ProviderMixin] | None

def product(module: type[Module] | None = None, imports: Iterable[type[ProviderMixin]] = [], products: Iterable[type[Product]] = [], provider: type[providers.Provider[Any]] = ..., bootstrap: bool = False) -> Callable[[type[PRODUCT]], type[PRODUCT]]:
    """Decorator for Product class

    Args:
        imports (Iterable[type[Component]], optional): List of components to be imported by the product. Defaults to [].
        products (Iterable[type[Product]], optional): List of products to be declared by the product. Defaults to [].
        provider (type[providers.Provider[Any]], optional): Provider class to be used. Defaults to providers.Singleton.

    Raises:
        TypeError: If the wrapped class is not a subclass of Product.

    Returns:
        Callable[[type[Dependent]], type[Dependent]]: Decorator function that wraps the dependent class.
    """
