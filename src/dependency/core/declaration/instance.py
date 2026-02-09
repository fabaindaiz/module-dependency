from typing import Any, Callable, Iterable, TypeVar
from dependency_injector import providers
from dependency.core.declaration.component import Component
from dependency.core.injection.mixin import ProviderMixin

_PROVIDERS = (
    providers.BaseSingleton,
    providers.Factory,
    providers.Resource,
)

T = TypeVar('T')

# TODO: review instance, what about other kinds of providers?
def instance(
    component: type[Component],
    provider: type[providers.Provider[Any]] = providers.Singleton,
    imports: Iterable[type[ProviderMixin]] = (),
    products: Iterable[type[ProviderMixin]] = (),
    bootstrap: bool = False,
) -> Callable[[type[T]], type[T]]:
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
    def wrap(cls: type[T]) -> type[T]:
        interface_cls: type = component.injection.interface_cls
        if not issubclass(cls, interface_cls):
            raise TypeError(f"Class {cls.__name__} must be a subclass of {interface_cls.__name__} to be used as an instance of component {component.__name__}")

        if not issubclass(provider, _PROVIDERS):
            raise TypeError(f"Instance {cls.__name__} has an invalid provider {provider.__name__} (allowed: {[p.__name__ for p in _PROVIDERS]})")

        component.init_injectable(
            wire_cls=[cls],
            imports=imports,
            products=products,
            provider=provider(cls),
            bootstrap=component.provide if bootstrap else None,
        )

        return cls
    return wrap
