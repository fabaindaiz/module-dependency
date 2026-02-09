from dependency.core.declaration.component import COMPONENT as COMPONENT, Component as Component
from dependency.core.declaration.validation import standalone_provider as standalone_provider
from dependency.core.injection.mixin import ProviderMixin as ProviderMixin
from dependency_injector import providers
from typing import Any, Callable, Iterable

def instance(imports: Iterable[type[ProviderMixin]] = (), products: Iterable[type[ProviderMixin]] = (), provider: type[providers.Provider[Any]] = ..., bootstrap: bool = False) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
    """Decorator for instance class

    Args:
        imports (Iterable[type[ProviderMixin]], optional): List of components to be imported by the provider. Defaults to ().
        products (Iterable[type[ProviderMixin]], optional): List of products to be declared by the provider. Defaults to ().
        provider (type[providers.Provider[Any]], optional): Provider to be used. Defaults to providers.Singleton.
        bootstrap (bool, optional): Whether the provider should be bootstrapped. Defaults to False.

    Raises:
        TypeError: If the wrapped class is not a subclass of Component declared base class.

    Returns:
        Callable[[type], Instance]: Decorator function that wraps the instance class and returns an Instance object.
    """
