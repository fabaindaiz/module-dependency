from dependency.core.injection.base import ProviderInjection as ProviderInjection
from dependency.core.injection.container import Container as Container
from dependency.core.injection.utils import provider_is_resolved as provider_is_resolved, raise_dependency_error as raise_dependency_error, raise_providers_error as raise_providers_error

class InjectionLoader:
    """Load and resolve dependencies for provider injections.
    """
    container: Container
    providers: list[ProviderInjection]
    resolved: list[ProviderInjection]
    def __init__(self, container: Container, providers: list[ProviderInjection]) -> None: ...
    def resolve_dependencies(self) -> None:
        """Resolve all dependencies.
        """
    def resolve_providers(self) -> None:
        """Resolve all providers in layers.
        """
    def resolve_products(self) -> None:
        """Check that all product dependencies are resolved.
        """
    def start_providers(self) -> None:
        """Start all resolved providers.
        """
