from dependency.core.module.component import Component
from dependency.core.module.provider import Provider

class Module:
    def __init__(self,
            module_cls,
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

    def get_providers(self):
        providers = self.providers.copy()
        for module in self.imports:
            providers.extend(module.providers())
        return providers
    
    def __repr__(self) -> str:
        return self.module_cls.__name__

def module(
        declaration: list[Component] = [],
        imports: list[Module] = [],
        bootstrap: list[Component] = [],

        providers: list[Provider] = [],
    ):
    def wrap(cls):
        class WrapModule(Module):
            def __init__(self):
                super().__init__(
                    module_cls=cls,
                    declaration=declaration,
                    imports=imports,
                    bootstrap=bootstrap,

                    providers=providers,
                )
        return WrapModule()
    return wrap