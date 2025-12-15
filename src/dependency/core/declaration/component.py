from typing import Callable, TypeVar
from dependency_injector.wiring import Provide, inject
from dependency.core.agrupation.module import Module
from dependency.core.declaration.base import ABCComponent, ABCInjectable
from dependency.core.injection.provider import ProviderInjection
from dependency.core.exceptions import DeclarationError

T = TypeVar('T')
COMPONENT = TypeVar('COMPONENT', bound='Component')

class Component(ABCComponent, ABCInjectable):
    """Component Base Class
    """
    def __init__(self,
        interface_cls: type[T],
        injection: ProviderInjection,
    ) -> None:
        super().__init__(interface_cls=interface_cls)
        self.injection: ProviderInjection = injection

def component(
    module: Module,
    interface: type[T],
) -> Callable[[type[COMPONENT]], COMPONENT]:
    """Decorator for Component class

    Args:
        module (Module): Module instance to register the component.
        interface (type[T]): Interface class to be used as a base class for the component.

    Raises:
        TypeError: If the wrapped class is not a subclass of Component.

    Returns:
        Callable[[type[COMPONENT]], COMPONENT]: Decorator function that wraps the component class.
    """
    def wrap(cls: type[COMPONENT]) -> COMPONENT:
        if not issubclass(cls, Component): # type: ignore
            raise TypeError(f"Class {cls} is not a subclass of {interface}")

        injection = ProviderInjection(
            name=cls.__name__,
            parent=module.injection,
        )

        class WrapComponent(cls):
            @inject
            def provide(self, instance: T = Provide[injection.reference]) -> T:
                if isinstance(instance, Provide): # type: ignore
                    raise DeclarationError(f"Component {cls.__name__} was not provided")
                return instance

        return WrapComponent( # type: ignore
            interface_cls=interface,
            injection=injection,
        )
    return wrap
