from dependency.core.agrupation.module import Module as Module
from dependency.core.declaration.product import Product as Product
from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.injection import ProviderInjection as ProviderInjection
from dependency.core.injection.mixin import ProviderMixin as ProviderMixin
from dependency_injector import providers as providers
from typing import Callable, Iterable, TypeVar

COMPONENT = TypeVar('COMPONENT', bound='Component')
INTERFACE = TypeVar('INTERFACE')

class Component(ProviderMixin):
    """Component Base Class
    """

def component(interface: type[INTERFACE], module: type[Module] | None = None, products: Iterable[type[Product]] = (), provider: providers.Provider[INTERFACE] | None = None) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
    """Decorator for Component class

    Args:
        interface (type): Interface class to be used as a base class for the component.
        module (type[Module], optional): Module where the component is registered. Defaults to None.

    Raises:
        TypeError: If the wrapped class is not a subclass of Component.

    Returns:
        Callable[[type[COMPONENT]], COMPONENT]: Decorator function that wraps the component class.
    """
