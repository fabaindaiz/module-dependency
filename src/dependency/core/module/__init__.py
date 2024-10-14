from abc import ABC
from typing import Callable
from dependency.core.declaration import Component, Provider

class Module(ABC):
    def __init__(self,
            module_cls: type,
            declaration: list[Component],
            imports: list["Module"],
            bootstrap: list[Component]
        ):
        self.module_cls = module_cls
        self.declaration = declaration
        self.imports = imports
        self.bootstrap = bootstrap

    def init_providers(self) -> list[Provider]:
        providers: list[Provider] = []
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
        declaration: list[Component] = [],
        imports: list[Module] = [],
        bootstrap: list[Component] = [],
    ) -> Callable[[type[Module]], Module]:
    def wrap(cls: type[Module]) -> Module:
        class WrapModule(cls): # type: ignore
            def __init__(self) -> None:
                super().__init__(
                    module_cls=cls,
                    declaration=declaration,
                    imports=imports,
                    bootstrap=bootstrap,
                )
        return WrapModule()
    return wrap