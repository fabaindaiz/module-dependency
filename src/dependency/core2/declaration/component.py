from typing import Any, Callable, Generic, TypeVar
from dependency_injector.wiring import Provide, inject
from dependency.core2.agrupation.module import Module
from dependency.core2.declaration.base import ABCComponent, ABCInjectable
from dependency.core2.injection.provider import ProviderInjection

T = TypeVar('T')
COMPONENT = TypeVar('COMPONENT', bound='Component')

class Component(ABCComponent, ABCInjectable):
    def __init__(self,
        interface_cls: type[T],
        injection: ProviderInjection,
    ) -> None:
        super().__init__(interface_cls=interface_cls)
        self.injection: ProviderInjection = injection
        self.imports: list[ABCInjectable] = []

def component(
    module: Module,
    interface: type[T],
) -> Callable[[type[COMPONENT]], COMPONENT]:
    def wrap(cls: type) -> Component:

        injection = ProviderInjection(
            name=cls.__name__,
            parent=module.injection,
        )

        class WrapComponent(Component):
            @inject
            def provide(self, instance: T = Provide[injection.reference]) -> T:
                return instance

        return WrapComponent(
            interface_cls=interface,
            injection=injection,
        )
    return wrap
