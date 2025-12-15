from typing import Callable
from dependency_injector import providers
from dependency.core2.declaration.base import ABCInstance
from dependency.core2.declaration.component import Component
from dependency.core2.injection.injectable import Injectable

class Instance(ABCInstance):
    def __init__(self,
        provided_cls: type,
    ) -> None:
        super().__init__(provided_cls=provided_cls)

def instance(
    component: Component,
    imports: list[Component] = [],
    products: list[type] = [],
    provider: type = providers.Singleton,
    bootstrap: bool = False,
) -> Callable[[type], Instance]:
    def wrap(cls: type) -> Instance:
        if not issubclass(cls, component.interface_cls):
            raise TypeError(f"Class {cls} is not a subclass of {component.interface_cls}")

        component.injection.set_instance(
            injectable = Injectable(
                component_cls=component.__class__,
                provided_cls=cls,
                provider_cls=provider,
                bootstrap=component.provide if bootstrap else None,
            ),
            imports = [
                component.injection
                for component in imports
            ],
        )

        return Instance(
            provided_cls=cls)
    return wrap
