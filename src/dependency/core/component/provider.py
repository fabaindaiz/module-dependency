from dependency_injector import providers
from typing import Any, Callable, cast
from dependency.core.component import Component
from dependency.core.container import Providable

class Provider:
    def __init__(self,
            provided_cls: type,
            imports: list[Component],
            provider: Providable
        ):
        self.provided_cls = provided_cls
        self.imports = imports
        self.provider = provider

    def __repr__(self) -> str:
        return self.provided_cls.__name__

def provider(
        component: type[Component],
        imports: list[type[Component]] = [],
        provider: type[providers.Provider[Any]] = providers.Singleton
    ) -> Callable[[type], Provider]:
    def wrap(cls: type) -> Provider:
        _component = cast(Component, component)
        _imports = cast(list[Component], imports)
        return Provider(
            provided_cls=cls,
            imports=_imports,
            provider=Providable(
                component=_component,
                provided_cls=cls,
                provider_cls=provider
            )
        )
    return wrap