from pprint import pformat
from typing import Callable, cast
from dependency_injector import providers
from dependency.core.container.injectable import Container, Injectable
from dependency.core.declaration.base import ABCProvider
from dependency.core.declaration.component import Component
from dependency.core.declaration.dependent import Dependent

class Provider(ABCProvider):
    """Provider Base Class
    """
    def __init__(self,
            imports: list[Component],
            dependents: list[type[Dependent]],
            provided_cls: type,
            inject: Injectable,
        ) -> None:
        super().__init__(provided_cls=provided_cls)
        self.provider = inject
        self.imports = imports
        self.dependents = dependents

        self.providers: list['Provider'] = []
    
    def declare_dependents(self, dependents: list[type[Dependent]]) -> None:
        self.unresolved_dependents: dict[str, list[str]] = {}
        for dependent in dependents:
            unresolved = [
                component.__repr__() for component in dependent._imports
                if component not in self.providers
            ]
            if len(unresolved) > 0:
                self.unresolved_dependents[dependent.__name__] = unresolved
        if len(self.unresolved_dependents) > 0:
            named_dependents = pformat(self.unresolved_dependents)
            raise TypeError(f"Provider {self} has unresolved dependents:\n{named_dependents}")
    
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
    """Decorator for Provider class

    Args:
        component (type[Component]): Component class to be used as a base class for the provider.
        imports (list[type[Component]], optional): List of components to be imported by the provider. Defaults to [].
        dependents (list[type[Dependent]], optional): List of dependents to be declared by the provider. Defaults to [].
        provider (type[providers.Provider], optional): Provider class to be used. Defaults to providers.Singleton.

    Raises:
        TypeError: If the wrapped class is not a subclass of Component declared base class.

    Returns:
        Callable[[type], Provider]: Decorator function that wraps the provider class.
    """
    # Cast due to mypy not supporting class decorators
    _component = cast(Component, component)
    _imports = cast(list[Component], imports)
    def wrap(cls: type) -> Provider:
        if not issubclass(cls, _component.base_cls):
            raise TypeError(f"Class {cls} is not a subclass of {_component.base_cls}")
        
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