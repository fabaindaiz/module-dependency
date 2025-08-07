import logging
from dependency.core.exceptions import DependencyError
from dependency.core.injection.base import ProviderInjection
from dependency.core.injection.utils import provider_unresolved
logger = logging.getLogger("DependencyLoader")

def provider_detect_error(
        provider: ProviderInjection,
        unresolved_providers: list[ProviderInjection],
        resolved_layers: list[list[ProviderInjection]]
    ) -> tuple[list[ProviderInjection], list[ProviderInjection]]:
    deps_circular: list[ProviderInjection] = []
    deps_missing: list[ProviderInjection] = []

    for dep in provider_unresolved(provider, resolved_layers):
        # TODO: Check for circular dependencies
        deps_missing.append(dep)

    logger.error(f"Provider {provider} has unresolved dependencies: {deps_missing}")
    return deps_circular, deps_missing

def raise_dependency_error(providers: list[ProviderInjection], resolved_layers: list[list[ProviderInjection]]) -> None:
    for provider in providers:
        provider_detect_error(provider, providers, resolved_layers)
    
    raise DependencyError("Dependencies cannot be resolved")