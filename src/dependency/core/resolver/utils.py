from dependency.core import Component, Provider

def dep_in_layers(dep: Component, layers: list[list[Provider]]):
    return any(
        issubclass(res._provider.base_cls, dep._base_cls)
        for layer in layers
        for res in layer
    )

def provider_is_resolved(provider: Provider, resolved_layers: list[list[Provider]]):
    dependencies = provider._imports
    return all(
        dep_in_layers(dep, resolved_layers)
        for dep in dependencies
    )

def provider_unresolved(provider: Provider, resolved_layers: list[list[Provider]]):
    dependencies = provider._imports
    return [
        dep
        for dep in dependencies
        if not dep_in_layers(dep, resolved_layers)
    ]