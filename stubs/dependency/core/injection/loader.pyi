from _typeshed import Incomplete
from dependency.core.injection.base import ProviderInjection as ProviderInjection
from dependency.core.injection.container import Container as Container

logger: Incomplete

class InjectionLoader:
    """Load and resolve dependencies for provider injections.
    """
    container: Container
    providers: list[ProviderInjection]
    def __init__(self, container: Container, providers: list[ProviderInjection]) -> None: ...
    def resolve_dependencies(self) -> list[list[ProviderInjection]]:
        """Resolve dependencies in layers.

        Returns:
            list[list[ProviderInjection]]: A list of layers, each containing resolved providers.
        """
