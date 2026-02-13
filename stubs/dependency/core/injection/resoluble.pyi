from dependency.core.injection.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection
from typing import Iterable

class ResolubleProvider(ProviderInjection):
    """Resoluable Provider Injection Class

    This class represents a provider injection that can be resolved and initialized.
    """
    partial_resolution: bool
    is_resolved: bool
    def __init__(self, name: str, interface_cls: type, parent: ContainerInjection | None = None) -> None: ...
    @property
    def imports(self) -> Iterable['ResolubleProvider']:
        """Return the set of imports for this provider injection."""
    @property
    def products(self) -> Iterable['ResolubleProvider']:
        """Return the set of products for this provider injection."""
    @property
    def needs_resolution(self) -> bool:
        """Return True if the provider injection needs resolution, False otherwise."""
    @property
    def import_resolved(self) -> bool: ...
    def as_import(self, provider: ResolubleProvider) -> ResolubleProvider: ...
    def as_product(self, provider: ResolubleProvider) -> ResolubleProvider: ...
    def inject(self) -> ResolubleProvider:
        """Mark the provider injection as resolved."""
    def add_dependencies(self, imports: Iterable['ResolubleProvider'], products: Iterable['ResolubleProvider'], partial_resolution: bool = False) -> None: ...
