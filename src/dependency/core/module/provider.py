
from dependency_injector import providers
from dependency.core.module.component import Component
from dependency.core.container import Providable
from typing import Any, TypeVar


class Provider:
    _provided_cls: type
    _imports: list[type[Component]]
    _provider: Providable

    def __repr__(self) -> str:
        return self._provided_cls.__name__

T = TypeVar('T')

def provider(
        component: type[Component],
        imports: list[type[Component]] = [],
        provider: type[providers.Provider] = providers.Singleton
    ):
    def wrap(cls):
        class WrapProvider(Provider):
            _provided_cls = cls
            _imports = imports
            _provider = Providable(
                component=component,
                provided_cls=cls,
                provider_cls=provider
            )
        return WrapProvider()
    return wrap