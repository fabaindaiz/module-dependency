import logging
from pprint import pformat
from dependency.core.injection.base import ProviderInjection
from dependency.core.injection.container import Container
from dependency.core.injection.utils import (
    provider_is_resolved,
    raise_providers_error,
    raise_dependency_error,
)
logger = logging.getLogger("DependencyLoader")

class InjectionLoader:
    """Load and resolve dependencies for provider injections.
    """
    def __init__(self, container: Container, providers: list[ProviderInjection]) -> None:
        self.container: Container = container
        self.providers: list[ProviderInjection] = providers
        self.resolved: list[ProviderInjection] = []
        super().__init__()
    
    def resolve_dependencies(self) -> None:
        """Resolve all dependencies.
        """
        self.resolve_providers()
        self.resolve_products()
        self.start_providers()
        logger.info("Dependencies resolved and initialized")

    # Strategy 1: Layered resolution
    # This strategy resolves providers by layers, ensuring that all dependencies
    # of a provider are resolved on previous layers before the provider is resolved.
    def resolve_providers(self) -> None:
        """Resolve all providers in layers.
        """
        resolved_layers: list[list[ProviderInjection]] = []
        unresolved_providers: list[ProviderInjection] = self.providers

        while unresolved_providers:
            new_layer = [
                provider.wire_provider(container=self.container)
                for provider in unresolved_providers
                if provider_is_resolved(provider.dependency, self.resolved)
            ]

            if len(new_layer) == 0:
                raise_providers_error(unresolved_providers, self.resolved)
            self.resolved.extend(new_layer)
            resolved_layers.append(new_layer)

            unresolved_providers = [
                provider
                for provider in unresolved_providers
                if provider not in new_layer
            ]
        named_layers = pformat(resolved_layers)
        logger.info(f"Resolved layers:\n{named_layers}")

    def resolve_products(self) -> None:
        """Check that all product dependencies are resolved.
        """
        unresolved_depends = [
            depends
            for provider in self.providers
            for depends in provider.depends
            if not provider_is_resolved(depends, self.resolved)]
        if unresolved_depends:
            raise_dependency_error(unresolved_depends, self.resolved)

    def start_providers(self) -> None:
        """Start all resolved providers.
        """
        for provider in self.resolved:
            provider.do_bootstrap()