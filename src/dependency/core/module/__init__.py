from typing import Callable, cast
from dependency.core.component import Component
from dependency.core.component.provider import Provider

class Module:
    def __init__(self,
            module_cls: type,
            declaration: list[Component],
            imports: list["Module"],
            bootstrap: list[Component],
            providers: list[Provider]   # TODO: create ProviderModule
        ):
        self.module_cls = module_cls
        self.declaration = declaration
        self.imports = imports
        self.bootstrap = bootstrap

        self.providers = providers

    def init_providers(self) -> list[Provider]:
        providers = self.providers.copy()
        for module in self.imports:
            providers.extend(module.init_providers())
        return providers
    
    def init_bootstrap(self) -> None:
        # start from inside to outside
        for module in self.imports:
            module.init_bootstrap()
        for component in self.bootstrap:
            component.provide()
    
    def __repr__(self) -> str:
        return self.module_cls.__name__

def module(
        declaration: list[type[Component]] = [],
        imports: list[type[Module]] = [],
        bootstrap: list[type[Component]] = [],
        providers: list[type[Provider]] = [],
    ) -> Callable[[type], Module]:
    def wrap(cls: type) -> Module:
        _declaration = cast(list[Component], declaration)
        _imports = cast(list[Module], imports)
        _bootstrap = cast(list[Component], bootstrap)
        _providers = cast(list[Provider], providers)
        return Module(
            module_cls=cls,
            declaration=_declaration,
            imports=_imports,
            bootstrap=_bootstrap,
            providers=_providers
        )
    return wrap