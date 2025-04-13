from dependency.core import ProviderModule, module
from example.plugins.module1.factory import CreatorComponent

@module(
    declaration=[
        CreatorComponent
    ],
    bootstrap=[
        
    ]
)
class ServicesModule(ProviderModule):
    def declare_providers(self): # type: ignore
        # Common providers
        from example.plugins.module1.factory.creators.creatorA import CreatorA
        return [
            CreatorA
        ]