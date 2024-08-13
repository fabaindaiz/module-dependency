from src.dependencies.resolver.utils import dep_in_layers, provider_unresolved

import logging
logger = logging.getLogger("DependencyLoader")

def provider_detect_error(provider, unresolved_providers, resolved_layers):
    deps_circular = []
    deps_missing = []

    for dep in provider_unresolved(provider, resolved_layers):
        # TODO: Check for circular dependencies
        deps_missing.append(dep.__name__)

    logger.critical(f"{provider.__name__} has unresolved dependencies: {deps_missing}")
    return deps_circular, deps_missing

def raise_dependency_error(providers, resolved_layers):
    for provider in providers:
        provider_detect_error(provider, providers, resolved_layers)
    
    raise ValueError("Dependencies cannot be resolved")