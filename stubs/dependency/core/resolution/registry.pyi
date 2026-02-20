from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.injection import ProviderInjection as ProviderInjection

class Registry:
    providers: set[ProviderInjection]
    @classmethod
    def register(cls, provider: ProviderInjection) -> None: ...
    @classmethod
    def validation(cls) -> None: ...
