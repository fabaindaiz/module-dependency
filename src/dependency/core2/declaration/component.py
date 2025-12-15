from typing import Callable, TypeVar
from dependency_injector.wiring import Provide, inject
from dependency.core2.agrupation.module import Module
from dependency.core2.declaration.base import ABCComponent, ABCInjectable
from dependency.core2.injection.provider import ProviderInjection
from dependency.core2.exceptions import DeclarationError

T = TypeVar('T')
COMPONENT = TypeVar('COMPONENT', bound='Component')

class Component(ABCComponent, ABCInjectable):
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
    def wrap(cls: type[COMPONENT]) -> COMPONENT:
        if not issubclass(cls, Component):
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

        return WrapComponent(
            interface_cls=interface,
            injection=injection,
        )
    return wrap
