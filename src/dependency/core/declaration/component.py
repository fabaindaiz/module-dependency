from abc import abstractmethod
from typing import Any, Callable, TypeVar
from dependency_injector.wiring import Provide, inject
from dependency.core.agrupation.module import Module
from dependency.core.declaration.base import ABCComponent
from dependency.core.injection.provider import ProviderInjection
from dependency.core.exceptions import DeclarationError

COMPONENT = TypeVar('COMPONENT', bound='Component')
INTERFACE = TypeVar('INTERFACE')

class Component(ABCComponent):
    """Component Base Class
    """
    def __init__(self,
        interface_cls: type[INTERFACE],
        injection: ProviderInjection,
    ) -> None:
        super().__init__(interface_cls=interface_cls)
        self.injection: ProviderInjection = injection

    @property
    def reference(self) -> str:
        """Return the reference name of the component."""
        return self.injection.reference

    @abstractmethod
    def provide(self) -> Any:
        pass

def component(
    module: Module,
    interface: type[INTERFACE],
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
        if not issubclass(cls, Component):
            raise TypeError(f"Class {cls} is not a subclass of {interface}")

        injection = ProviderInjection(
            name=cls.__name__,
            parent=module.injection,
        )

        class WrapComponent(cls): # type: ignore
            @inject
            def provide(self, instance: INTERFACE = Provide[injection.reference]) -> INTERFACE:
                if isinstance(instance, Provide): # type: ignore
                    raise DeclarationError(f"Component {cls.__name__} was not provided")
                return instance

        return WrapComponent(
            interface_cls=interface,
            injection=injection,
        )
    return wrap
