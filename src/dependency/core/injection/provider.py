from typing import Any, Generator, Optional
from dependency_injector import providers
from dependency.core.injection.base import BaseInjection, ContainerInjection
from dependency.core.injection.injectable import Injectable
from dependency.core.exceptions import DeclarationError

class ProviderInjection(BaseInjection):
    """Provider Injection Class
    """
    def __init__(self,
        name: str,
        parent: Optional["ContainerInjection"] = None
    ) -> None:
        super().__init__(name=name, parent=parent)
        self.__injectable: Optional[Injectable] = None
        self.__imports: list[ProviderInjection] = []

    @property
    def injectable(self) -> Injectable:
        """Return the injectable instance."""
        if not self.__injectable:
            raise DeclarationError(f"Implementation for provider {self.name} was not set")
        return self.__injectable

    def set_instance(self,
        injectable: Injectable,
        imports: list['ProviderInjection'] = [],
    ) -> None:
        """Set the injectable instance and its imports."""
        self.__injectable = injectable
        self.__imports = imports
        if self.parent:
            self.parent.childs.append(self)

    def inject_cls(self) -> providers.Provider[Any]:
        """Return the provider instance."""
        return self.injectable.provider()

    def resolve_providers(self) -> Generator[Injectable, None, None]:
        """Inject all imports into the current injectable."""
        self.injectable.imports = [
            provider.injectable
            for provider in self.__imports
        ]
        yield self.injectable
