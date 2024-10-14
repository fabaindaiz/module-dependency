from abc import abstractmethod
from dependency.core.module import Module, module
from dependency.core.declaration import Provider

__all__ = [
    "ProviderModule",
    "module"
]

class ProviderModule(Module):
    @abstractmethod
    def declare_providers(self) -> list[Provider]:
        pass

    def init_providers(self) -> list[Provider]:
        providers: list[Provider] = self.declare_providers()
        for module in self.imports:
            providers.extend(module.init_providers())
        return providers