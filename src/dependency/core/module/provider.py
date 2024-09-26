
from dependency.core.module.component import Component
from dependency.core.container import Providable
from dependency_injector import providers

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
        component,
        imports = [],
        provider = providers.Singleton
    ):
    def wrap(cls) -> Provider:
        return Provider(
            provided_cls=cls,
            imports=imports,
            provider=Providable(
                component=component,
                provided_cls=cls,
                provider_cls=provider
            )
        )
    return wrap