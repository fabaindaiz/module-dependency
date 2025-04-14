from pprint import pformat
from typing import Callable, cast
from dependency_injector import providers
from dependency.core.container.injectable import Container, Injectable
from dependency.core.declaration.base import ABCProvider
from dependency.core.declaration.component import Component
from dependency.core.declaration.dependent import Dependent

class Provider(ABCProvider):
    def __init__(self,
            imports: list[Component],
            dependents: list[type[Dependent]],
            provided_cls: type,
            inject: Injectable,
        ):
        super().__init__(provided_cls=provided_cls)
        self.provider = inject
        self.imports = imports
        self.dependents = dependents

        self.providers: list['Provider'] = []
    
    def declare_dependents(self, dependents: list[type[Dependent]]) -> None:
        self.unresolved_dependents: dict[str, list[str]] = {}
        for dependent in dependents:
            unresolved = [
                component.__repr__() for component in dependent.imports
                if component not in self.providers
            ]
            if len(unresolved) > 0:
                self.unresolved_dependents[dependent.__name__] = unresolved # TODO: names
        if len(self.unresolved_dependents) > 0:
            raise TypeError(f"Dependent {self} has unresolved dependencies:\n{pformat(self.unresolved_dependents)}")
    
    def resolve(self, container: Container, providers: list['Provider']) -> None:
        self.providers = providers
        self.declare_dependents(self.dependents)
        self.provider.populate_container(container)

def provider(
        component: type[Component],
        imports: list[type[Component]] = [],
        dependents: list[type[Dependent]] = [],
        provider: type[providers.Provider] = providers.Singleton
    ) -> Callable[[type], Provider]:
    def wrap(cls: type) -> Provider:
        _component = cast(Component, component)
        _imports = cast(list[Component], imports)
        provider_wrap = Provider(
            imports=_imports,
            dependents=dependents,
            provided_cls=cls,
            inject=Injectable(
                inject_name=_component.base_cls.__name__,
                inject_cls=_component.__class__,
                provided_cls=cls,
                provider_cls=provider
            )
        )
        _component.provider = provider_wrap
        return provider_wrap
    return wrap