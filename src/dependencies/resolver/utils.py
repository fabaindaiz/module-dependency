
def dep_in_layers(dep, layers):
    return any(
        issubclass(res, dep)
        for layer in layers
        for res in layer
    )

def provider_is_resolved(provider, resolved_layers):
    dependencies = provider.depends()
    return all(
        dep_in_layers(dep, resolved_layers)
        for dep in dependencies
    )

def provider_unresolved(provider, resolved_layers):
    dependencies = provider.depends()
    return [
        dep
        for dep in dependencies
        if not dep_in_layers(dep, resolved_layers)
    ]