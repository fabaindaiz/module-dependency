import logging
from typing import Any, Callable, Iterable, Optional, TypeVar
from dependency_injector import providers
from dependency.core.agrupation.module import Module
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.injection import ProviderInjection
from dependency.core.injection.mixin import ProviderMixin
_logger = logging.getLogger("dependency.loader")

_PROVIDERS = (
    providers.BaseSingleton,
    providers.Factory,
    providers.Resource,
)

PRODUCT = TypeVar('PRODUCT', bound='Product')

class Product(ProviderMixin):
    """Product Base Class
    """
    implicit_component: Optional[type[ProviderMixin]] = None

# TODO: Products can be provided in components too
def product(
    module: Optional[type[Module]] = None,
    imports: Iterable[type[ProviderMixin]] = [],
    products: Iterable[type[Product]] = [],
    provider: type[providers.Provider[Any]] = providers.Singleton,
    bootstrap: bool = False,
) -> Callable[[type[PRODUCT]], type[PRODUCT]]:
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
    def wrap(cls: type[PRODUCT]) -> type[PRODUCT]:
        if not issubclass(cls, Product):
            raise TypeError(f"Class {cls} has decorator @product but is not a subclass of Product")

        if cls.implicit_component is not None:
            _logger.debug(f"Product {cls.__name__} implicit component assigned: {cls.implicit_component.__name__}")
            return cls

        if not issubclass(provider, _PROVIDERS):
            raise TypeError(f"Product {cls.__name__} has an invalid provider {provider.__name__} (allowed: {[p.__name__ for p in _PROVIDERS]})")

        cls.injection = ProviderInjection(
            name=cls.__name__,
            interface_cls=cls,
            parent=module.injection if module else None,
        )
        cls.injection.set_instance(
            injectable = Injectable(
                component_cls=cls,
                provided_cls=[cls],
                provider=provider(cls),
                imports=(
                    component.injection.injectable
                    for component in imports
                ),
                products=(
                    product.injection.injectable
                    for product in products
                ),
                bootstrap=cls.provide if bootstrap else None,
            )
        )

        return cls
    return wrap
