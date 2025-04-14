from abc import ABC
from typing import Callable, cast
from dependency.core.common.exceptions import DependencyError
from dependency.core.declaration import Component, Provider

class Module(ABC):
    """Module Base Class
    """
    def __init__(self,
            module_cls: type,
            imports: list["Module"],
            declaration: list[Component],
            bootstrap: list[Component]
        ):
        self.module_cls = module_cls
        self.imports = imports
        self.declaration = declaration
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
                raise DependencyError(f"Failed to bootstrap {component}: {e}") from e
    
    def __repr__(self) -> str:
        return self.module_cls.__name__

def module(
        imports: list[type[Module]] = [],
        declaration: list[type[Component]] = [],
        bootstrap: list[type[Component]] = [],
    ) -> Callable[[type[Module]], Module]:
    """Decorator for Module class

    Args:
        imports (list[type[Module]], optional): List of modules to be imported by the module. Defaults to [].
        declaration (list[type[Component]], optional): List of components to be declared by the module. Defaults to [].
        bootstrap (list[type[Component]], optional): List of components to be bootstrapped by the module. Defaults to [].

    Raises:
        TypeError: If the wrapped class is not a subclass of Module.

    Returns:
        Callable[[type[Module]], Module]: Decorator function that wraps the module class.
    """
    # Cast due to mypy not supporting class decorators
    _declaration = cast(list[Component], declaration)
    _imports = cast(list[Module], imports)
    _bootstrap = cast(list[Component], bootstrap)
    def wrap(cls: type[Module]) -> Module:
        if not issubclass(cls, Module):
            raise TypeError(f"Class {cls} is not a subclass of Module")

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