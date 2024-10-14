from typing import Any, Callable
from dependency_injector import providers
from dependency.core.container.injectable import Injectable
from dependency.core.declaration.base import ABCComponent, ABCProvider
from dependency.core.declaration.component import Component

class Provider(ABCProvider):
    def __init__(self,
            provided_cls: type,
            imports: list[ABCComponent],
            inject: Injectable
        ):
        super().__init__(provided_cls=provided_cls)
        self.imports = imports
        self.provider = inject

    def __repr__(self) -> str:
        return self.provided_cls.__name__

def provider(
        component: Component,
        imports: list[Component] = [],
        provider: type[providers.Provider[Any]] = providers.Singleton
    ) -> Callable[[type], Provider]:
    def wrap(cls: type) -> Provider:
        provider_wrap = Provider(
            provided_cls=cls,
            imports=imports,
            inject=Injectable(
                inject_name=component.base_cls.__name__,
                inject_cls=component.__class__,
                provided_cls=cls,
                provider_cls=provider
            )
        )
        component.provider = provider_wrap
        return provider_wrap
    return wrap