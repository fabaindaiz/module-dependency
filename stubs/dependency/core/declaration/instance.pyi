from dependency.core.declaration.component import Component as Component
from dependency.core.injection.mixin import ProviderMixin as ProviderMixin
from dependency_injector import providers
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

def instance(component: type[Component], provider: type[providers.Provider[Any]] = ..., imports: Iterable[type[ProviderMixin]] = (), products: Iterable[type[ProviderMixin]] = (), bootstrap: bool = False) -> Callable[[type[T]], type[T]]:
    """Decorator for instance class

    Args:
        component (type[Component]): Component class to be used as a base class for the provider.
        imports (Iterable[type[ProviderMixin]], optional): List of components to be imported by the provider. Defaults to ().
        products (Iterable[type[ProviderMixin]], optional): List of products to be declared by the provider. Defaults to ().
        provider (type[providers.Provider[Any]], optional): Provider to be used. Defaults to providers.Singleton.
        bootstrap (bool, optional): Whether the provider should be bootstrapped. Defaults to False.

    Raises:
        TypeError: If the wrapped class is not a subclass of Component declared base class.

    Returns:
        Callable[[type], Instance]: Decorator function that wraps the instance class and returns an Instance object.
    """
