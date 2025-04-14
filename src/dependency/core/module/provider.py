from abc import abstractmethod
from dependency.core.module.base import Module
from dependency.core.declaration import Provider

class ProviderModule(Module):
    """Provider Module Base Class
    """
    @abstractmethod
    def declare_providers(self) -> list[Provider]:
        pass

    def init_providers(self) -> list[Provider]:
        providers: list[Provider] = self.declare_providers()
        for module in self.imports:
            providers.extend(module.init_providers())
        return providers