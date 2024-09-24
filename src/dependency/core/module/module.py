from dependency.core.module.component import Component
from dependency.core.module.provider import Provider
from typing import Generic, TypeVar

T = TypeVar('T')

class Module(Generic[T]):
    _module_cls: type
    _declaration: list[type[Component]]
    _imports: list[type["Module"]]
    _bootstrap: list[type[Component]]

    # TODO: extract to Selector Module
    _providers: list[Provider]
    def providers(self) -> list[Provider]:
        providers = self._providers
        for module in self._imports:
            providers.extend(module.providers())
        return providers
    
    def __repr__(self) -> str:
        return self._module_cls.__name__

def module(
        declaration: list[type[Component]] = [],
        imports: list[type[Module]] = [],
        providers: list = [],
        bootstrap: list[type[Component]] = [],
    ):
    def wrap(cls):
        class WrapModule(Module):
            _module_cls = cls
            _declaration = declaration
            _imports = imports
            _providers = providers
            _bootstrap = bootstrap
        return WrapModule()
    return wrap