
def dep_in_layers(dep, layers):
    return any(
        issubclass(res._component.__class__, dep.__class__)
        for layer in layers
        for res in layer
    )

def provider_is_resolved(provider, resolved_layers):
    dependencies = provider._imports
    return all(
        dep_in_layers(dep, resolved_layers)
        for dep in dependencies
    )

def provider_unresolved(provider, resolved_layers):
    dependencies = provider._imports
    return [
        dep
        for dep in dependencies
        if not dep_in_layers(dep, resolved_layers)
    ]