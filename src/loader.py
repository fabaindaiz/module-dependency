from dependency_injector import containers, providers
from src.container import Container

def all_dependencies_resolved(dependencies, resolved_layers):
    return all(
        any(
            issubclass(dep, res)
            for res in resolved
        )
        for dep in dependencies
        for resolved in resolved_layers)

def resolve_dependencies(unresolved_layers):
    resolved_layers = []

    while unresolved_layers:
        new_layer = []

        for provider in unresolved_layers:
            dependencies = provider.depends()
            if all_dependencies_resolved(dependencies, resolved_layers):
                new_layer.append(provider)

        if not new_layer:
            raise ValueError("No se pueden resolver las dependencias, puede haber un ciclo")

        resolved_layers.append(new_layer)
        unresolved_layers = [p for p in unresolved_layers if p not in new_layer]

    return resolved_layers

def populate_layers(unresolved: list, config: dict):
    resolved = resolve_dependencies(unresolved)

    for layer in resolved:
        populate(layer, config)

def populate(resolved: list, config: dict):
        base = Container()
        layer = containers.DynamicContainer()
        layer.config = providers.Configuration()

        for provided_cls in resolved:
            setattr(layer, provided_cls.name(), providers.Container(provided_cls, config=layer.config))

        base.override(layer)
        base.config.from_dict(config)
        base.loader()