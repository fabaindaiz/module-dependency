from dependency.core.module.provider import ProviderModule, module
from example.module.creation.afactory import CreatorComponent

@module(
    declaration=[
        CreatorComponent
    ],
    imports=[
    ],
    bootstrap=[
        CreatorComponent
    ]
)
class MainModule(ProviderModule):
    def declare_providers(self): # type: ignore
        from example.module.creation.afactory.concrete import ConcreteCreator
        return [
            ConcreteCreator
        ]