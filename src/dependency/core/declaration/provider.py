from typing import Any, Callable, cast
from dependency_injector import providers
from dependency.core.container.injectable import Container, Injectable
from dependency.core.declaration.base import ABCComponent, ABCProvider, ABCDependent
from dependency.core.declaration.component import Component
from dependency.core.declaration.dependent import Dependent

class Provider(ABCProvider):
    def __init__(self,
            provided_cls: type,
            imports: list[Component],
            inject: Injectable,
            dependents: list[Dependent],
        ):
        super().__init__(provided_cls=provided_cls)
        self.imports = imports
        self.provider = inject
        self.dependents = dependents

        self.providers: list['Provider'] = []
    
    def declare_dependents(self, dependents: list[Dependent]) -> None:
        self.unresolved_dependents: dict[str, list[Component]] = {}
        for dependent in dependents:
            unresolved = [
                component for component in dependent.imports
                if component not in self.providers
            ]
            if len(unresolved) > 0:
                self.unresolved_dependents[dependent.__class__.__name__] = unresolved # TODO: names
        if len(self.unresolved_dependents) > 0:
            raise TypeError(f"Dependent {dependent} has unresolved dependencies: {self.unresolved_dependents}")
    
    def resolve(self, container: Container, providers: list['Provider']) -> None:
        self.providers = providers
        self.declare_dependents(self.dependents)
        self.provider.populate_container(container)

    def __repr__(self) -> str:
        return self.provided_cls.__name__

def provider(
        component: type[Component],
        imports: list[type[Component]] = [],
        dependents: list[type[Dependent]] = [],
        provider: type[providers.Provider[Any]] = providers.Singleton
    ) -> Callable[[type], Provider]:
    def wrap(cls: type) -> Provider:
        _component = cast(Component, component)
        _imports = cast(list[Component], imports)
        _dependents = cast(list[Dependent], dependents)
        provider_wrap = Provider(
            provided_cls=cls,
            imports=_imports,
            dependents=_dependents,
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