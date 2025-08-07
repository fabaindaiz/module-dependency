from dependency.core.injection.base import ProviderInjection

def dep_in_layers(dep: ProviderInjection, layers: list[list[ProviderInjection]]) -> bool:
    return any(
        issubclass(res.provided_cls, dep.component)
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