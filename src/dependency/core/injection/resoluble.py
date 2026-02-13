from typing import Iterable, Optional
from dependency.core.injection.injection import ContainerInjection, ProviderInjection

class ResolubleProvider(ProviderInjection):
    """Resoluable Provider Injection Class

    This class represents a provider injection that can be resolved and initialized.
    """
    def __init__(self,
        name: str,
        interface_cls: type,
        parent: Optional['ContainerInjection'] = None
    ) -> None:
        super().__init__(name=name, interface_cls=interface_cls, parent=parent)
        self.__imports: set['ResolubleProvider'] = set()
        self.__products: set['ResolubleProvider'] = set()
        self.__import_of: set['ResolubleProvider'] = set()
        self.__product_of: set['ResolubleProvider'] = set()

        self.partial_resolution: bool = False
        self.is_resolved: bool = False

    @property
    def imports(self) -> Iterable['ResolubleProvider']:
        """Return the set of imports for this provider injection."""
        return self.__imports

    @property
    def products(self) -> Iterable['ResolubleProvider']:
        """Return the set of products for this provider injection."""
        return self.__products

    @property
    def needs_resolution(self) -> bool:
        """Return True if the provider injection needs resolution, False otherwise."""
        return bool(self.__import_of)

    @property
    def import_resolved(self) -> bool:
        if self.partial_resolution and self.__product_of:
            return True

        return all(
            implementation.is_resolved
            for implementation in self.__imports
        )

    def as_import(self, provider: 'ResolubleProvider') -> 'ResolubleProvider':
        self.__import_of.add(provider)
        return self

    def as_product(self, provider: 'ResolubleProvider') -> 'ResolubleProvider':
        self.__product_of.add(provider)
        return self

    def inject(self) -> 'ResolubleProvider':
        """Mark the provider injection as resolved."""
        self.is_resolved = True
        self.injectable.inject()
        return self

    def add_dependencies(self,
        imports: Iterable['ResolubleProvider'],
        products: Iterable['ResolubleProvider'],
        partial_resolution: bool = False,
    ) -> None:
        self.__imports.update(imports)
        self.__products.update(products)
        self.partial_resolution = partial_resolution
