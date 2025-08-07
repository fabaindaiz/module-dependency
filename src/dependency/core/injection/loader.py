import logging
from pprint import pformat
from dependency.core.agrupation.plugin import Plugin
from dependency.core.injection.base import ProviderInjection
from dependency.core.injection.container import Container
from dependency.core.injection.errors import raise_dependency_error
from dependency.core.injection.utils import provider_is_resolved

logger = logging.getLogger("DependencyLoader")

class InjectionLoader:
    def __init__(self, container: Container, plugins: list[Plugin]) -> None:
        for plugin in plugins:
            plugin.set_container(container)
        self.container: Container = container
        self.plugins: list[Plugin] = plugins
        self.providers: list[ProviderInjection] = [
            provider 
            for plugin in plugins
            for provider in plugin.injection.child_inject()
        ]
        
    def resolve_dependencies(self) -> list[list[ProviderInjection]]:
        unresolved_providers: list[ProviderInjection] = self.providers
        resolved_layers: list[list[ProviderInjection]] = []

        while unresolved_providers:
            new_layer = [
                provider
                for provider in unresolved_providers
                if provider_is_resolved(provider, resolved_layers)
            ]

            if len(new_layer) == 0:
                raise_dependency_error(unresolved_providers, resolved_layers)
            resolved_layers.append(new_layer)

            unresolved_providers = [
                provider
                for provider in unresolved_providers
                if provider not in new_layer
            ]
        named_layers = pformat(resolved_layers)
        logger.info(f"Resolved layers:\n{named_layers}")
        self.container.check_dependencies()
        self.container.init_resources()

        for resolved_layer in resolved_layers:
            for provider in resolved_layer:
                provider.child_wire(self.container)
                provider.bootstrap_provider()
        
        logger.info("Dependencies resolved and injected")
        return resolved_layers