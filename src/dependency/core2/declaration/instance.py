from dependency_injector import providers
from typing import Any, Callable, Optional, TypeVar
from dependency.core2.declaration.base import ABCInstance, ABCInjectable
from dependency.core2.declaration.component import Component
from dependency.core2.resolution.implementation import Implementation

T = TypeVar('T')

class Instance(ABCInstance):
    def __init__(self,
        provided_cls: type,
    ) -> None:
        super().__init__(provided_cls=provided_cls)

def instance(
    component: Component,
    imports: list[ABCInjectable] = [],
    products: list[ABCInjectable] = [],
    provider: type = providers.Singleton,
    bootstrap: bool = False,
) -> Callable[[type], Instance]:
    def wrap(cls: type) -> Instance:
        if not issubclass(cls, component.interface_cls):
            raise TypeError(f"Class {cls} is not a subclass of {component.interface_cls}")

        component.imports = imports
        component.injection.implementation = Implementation(
            provider_cls=provider,
            provided_cls=cls,
            component_cls=component.__class__,
            bootstrap=component.provide if bootstrap else None,
        )

        return Instance(
            provided_cls=cls)
    return wrap
