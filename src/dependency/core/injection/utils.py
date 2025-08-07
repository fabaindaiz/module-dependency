import logging
from dependency.core.exceptions import DependencyError
from dependency.core.injection.base import ProviderInjection
logger = logging.getLogger("DependencyLoader")

def dep_in_layers(dep: ProviderInjection, layers: list[list[ProviderInjection]]) -> bool:
    return any(
        issubclass(res.provided_cls, dep.interface_cls)
        for layer in layers
        for res in layer
    )

def provider_is_resolved(provider: ProviderInjection, resolved_layers: list[list[ProviderInjection]]) -> bool:
    dependencies = provider.imports
    return all(
        dep_in_layers(dep, resolved_layers)
        for dep in dependencies
    )

def provider_unresolved(provider: ProviderInjection, resolved_layers: list[list[ProviderInjection]]) -> list[ProviderInjection]:
    dependencies = provider.imports
    return [
        dep
        for dep in dependencies
        if not dep_in_layers(dep, resolved_layers)
    ]

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