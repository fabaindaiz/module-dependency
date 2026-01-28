import logging
from typing import Callable, Iterable, Optional, TypeVar
from dependency_injector import providers
from dependency.core.agrupation.module import Module
from dependency.core.declaration.product import Product
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.injection import ProviderInjection
from dependency.core.injection.mixin import ProviderMixin
_logger = logging.getLogger("dependency.loader")

COMPONENT = TypeVar('COMPONENT', bound='Component')
INTERFACE = TypeVar('INTERFACE')

class Component(ProviderMixin):
    """Component Base Class
    """

def component(
    interface: type[INTERFACE],
    module: Optional[type[Module]] = None,
    products: Iterable[type[Product]] = (),
    provider: Optional[providers.Provider[INTERFACE]] = None,
) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
    """Decorator for Component class

    Args:
        interface (type): Interface class to be used as a base class for the component.
        module (type[Module], optional): Module where the component is registered. Defaults to None.

    Raises:
        TypeError: If the wrapped class is not a subclass of Component.

    Returns:
        Callable[[type[COMPONENT]], COMPONENT]: Decorator function that wraps the component class.
    """
    def wrap(cls: type[COMPONENT]) -> type[COMPONENT]:
        if not issubclass(cls, Component):
            raise TypeError(f"Class {cls} has decorator @component but is not a subclass of Component")

        if module is None:
            _logger.warning(f"Component {cls.__name__} has no parent module (consider registering)")

        cls.injection = ProviderInjection(
            name=cls.__name__,
            interface_cls=interface,
            parent=module.injection if module else None,
        )

        if provider is not None:
            products_list: list[type[Product]] = list(products)
            if len(products_list) == 0:
                _logger.warning(f"Component {cls.__name__} has a provider but no provided classes")

            cls.injection.set_instance(
                injectable = Injectable(
                    component_cls=cls,
                    provided_cls=products_list,
                    provider=provider,
                    products=(
                        product.injection.injectable
                        for product in products_list
                    ),
                )
            )

        return cls
    return wrap
