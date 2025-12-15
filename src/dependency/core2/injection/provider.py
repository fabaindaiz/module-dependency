from typing import Any, Generator, Optional
from dependency.core2.injection.base import BaseInjection, ContainerInjection
from dependency.core2.resolution.implementation import Implementation
from dependency.core2.exceptions import DeclarationError

class ProviderInjection(BaseInjection):
    def __init__(self,
        name: str,
        parent: Optional["ContainerInjection"] = None
    ) -> None:
        super().__init__(name=name, parent=parent)
        self.__implementation: Optional[Implementation] = None

    @property
    def implementation(self) -> Implementation:
        if not self.__implementation:
            raise DeclarationError("Implementation is not set.")
        return self.__implementation

    @implementation.setter
    def implementation(self, implementation: Implementation) -> None:
        self.__implementation = implementation

    def inject_cls(self) -> Any:
        """Return the provider instance."""
        return self.implementation.provide()

    def resolve_providers(self) -> Generator[Implementation, None, None]:
        yield self.implementation
