import logging
from typing import Callable, Optional, TypeVar
from dependency_injector import providers
from dependency.core.agrupation.module import Module
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.provider import ProviderInjection
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
    provided: list[type] = [],
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
            raise TypeError(f"Class {cls} is not a subclass of Component")

        if module is None:
            _logger.warning(f"Component {cls.__name__} is not registered to any module")

        cls.injection = ProviderInjection(
            name=cls.__name__,
            interface_cls=interface,
            parent=module.injection if module else None,
        )

        # TODO: Complete this
        if provider is not None:
            cls.injection.set_instance(
                injectable = Injectable(
                    component_cls=cls,
                    provided_cls=provided,
                    provider=provider,
                    imports=(),
                    products=(),
                )
            )

        return cls
    return wrap
