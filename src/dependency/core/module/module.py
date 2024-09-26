from dependency.core.module.component import Component
from dependency.core.module.provider import Provider

class Module:
    def __init__(self,
            module_cls: type,
            declaration: list[Component],
            imports: list["Module"],
            bootstrap: list[Component],

            providers: list[Provider],
        ):
        self.module_cls = module_cls
        self.declaration = declaration
        self.imports = imports
        self.bootstrap = bootstrap

        self.providers = providers

    def init_providers(self):
        providers = self.providers.copy()
        for module in self.imports:
            providers.extend(module.init_providers())
        return providers
    
    def init_bootstrap(self):
        for component in self.bootstrap:
            component.provide()
        for module in self.imports:
            module.init_bootstrap()
    
    def __repr__(self) -> str:
        return self.module_cls.__name__

def module(
        declaration = [],
        imports = [],
        bootstrap = [],

        providers = [],
    ):
    def wrap(cls) -> Module:
        return Module(
            module_cls=cls,
            declaration=declaration,
            imports=imports,
            bootstrap=bootstrap,

            providers=providers,
        )
    return wrap