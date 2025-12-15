from typing import Any, Generator, Optional
from dependency.core2.injection.base import BaseInjection, ContainerInjection
from dependency.core2.injection.injectable import Injectable
from dependency.core2.exceptions import DeclarationError

class ProviderInjection(BaseInjection):
    def __init__(self,
        name: str,
        parent: Optional["ContainerInjection"] = None
    ) -> None:
        super().__init__(name=name, parent=parent)
        self.__injectable: Optional[Injectable] = None
        self.__imports: list[ProviderInjection] = []

    @property
    def injectable(self) -> Injectable:
        if not self.__injectable:
            raise DeclarationError("Injectable is not set.")
        return self.__injectable

    def set_instance(self,
        injectable: Injectable,
        imports: list['ProviderInjection'] = [],
    ) -> None:
        self.__injectable = injectable
        self.__imports = imports

    def inject_cls(self) -> Any:
        """Return the provider instance."""
        return self.injectable.provide()

    def resolve_providers(self) -> Generator[Injectable, None, None]:
        self.injectable.imports = [
            provider.injectable
            for provider in self.__imports
        ]
        yield self.injectable
