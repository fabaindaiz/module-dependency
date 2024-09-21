from dependency.core import Component, Provider
from dependency.core.resolver.utils import dep_in_layers, provider_unresolved

def provider_detect_error(
        provider: Provider,
        unresolved_providers: list[Provider],
        resolved_layers: list[list[Provider]]
    ):
    deps_circular: list[Component] = []
    deps_missing: list[Component] = []

    for dep in provider_unresolved(provider, resolved_layers):
        # TODO: Check for circular dependencies
        deps_missing.append(dep)

    print(f"{provider} has unresolved dependencies: {deps_missing}")
    return deps_circular, deps_missing

def raise_dependency_error(
        providers: list[Provider],
        resolved_layers: list[list[Provider]]
    ):
    for provider in providers:
        provider_detect_error(provider, providers, resolved_layers)
    
    raise ValueError("Dependencies cannot be resolved")