from abc import ABC
from typing import Callable, cast
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
            try:
                if component.provider is not None:
                    component.provide()
            except Exception as e:
                raise Exception(f"Failed to bootstrap {component}: {e}") from e
    
    def __repr__(self) -> str:
        return self.module_cls.__name__

def module(
        declaration: list[type[Component]] = [],
        imports: list[type[Module]] = [],
        bootstrap: list[type[Component]] = [],
    ) -> Callable[[type[Module]], Module]:
    def wrap(cls: type[Module]) -> Module:
        _declaration = cast(list[Component], declaration)
        _imports = cast(list[Module], imports)
        _bootstrap = cast(list[Component], bootstrap)
        class WrapModule(cls): # type: ignore
            def __init__(self) -> None:
                super().__init__(
                    module_cls=cls,
                    declaration=_declaration,
                    imports=_imports,
                    bootstrap=_bootstrap,
                )
        return WrapModule()
    return wrap