from dependency.core.declaration.base import ABCInstance
from dependency.core.declaration.component import Component
from dependency.core.declaration.product import Product
from dependency_injector import providers as providers
from typing import Any, Callable

__all__ = ['Instance', 'instance', 'providers']

class Instance(ABCInstance):
    """Instance Base Class
    """
    def __init__(self, provided_cls: type) -> None: ...

def instance(component: Component, imports: list[Component] = [], products: list[Product] = [], provider: type[providers.Provider[Any]] = ..., bootstrap: bool = False) -> Callable[[type], Instance]:
    """Decorator for instance class

    Args:
        component (type[Component]): Component class to be used as a base class for the provider.
        imports (list[type[Component]], optional): List of components to be imported by the provider. Defaults to [].
        products (list[type[Product]], optional): List of products to be declared by the provider. Defaults to [].
        provider (type[providers.Provider], optional): Provider class to be used. Defaults to providers.Singleton.
        bootstrap (bool, optional): Whether the provider should be bootstrapped. Defaults to False.
        
    Raises:
        TypeError: If the wrapped class is not a subclass of Component declared base class.

    Returns:
        Callable[[type], Instance]: Decorator function that wraps the instance class and returns an Instance object.
    """
