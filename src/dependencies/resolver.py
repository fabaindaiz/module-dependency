
def all_dependencies_resolved(dependencies, resolved_layers):
    if not dependencies:
        return True
    if not resolved_layers:
        return False
    return all(
        any(
            issubclass(res, dep)
            for resolved in resolved_layers
            for res in resolved
        )
        for dep in dependencies)

def resolve_dependency_layers(unresolved_layers):
    resolved_layers = []

    while unresolved_layers:
        new_layer = []

        for provider in unresolved_layers:
            dependencies = provider.depends()
            print(f"Provider: {provider.name()} - Dependencies: {dependencies} - Resolved layers: {resolved_layers}")
            if all_dependencies_resolved(dependencies, resolved_layers):
                new_layer.append(provider)

        if not new_layer:
            raise ValueError("No se pueden resolver las dependencias, puede haber un ciclo")

        resolved_layers.append(new_layer)
        unresolved_layers = [p for p in unresolved_layers if p not in new_layer]

    return resolved_layers