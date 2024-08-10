from dependency_injector import containers, providers
from src.dependencies.resolver import resolve_dependency_layers

class Container(containers.DynamicContainer):
    config: providers.Configuration = providers.Dependency()

def resolve_dependency(unresolved: list, config: dict):
    resolved_layers = resolve_dependency_layers(unresolved)
    for resolved_layer in resolved_layers:
        populate_layer(resolved_layer, config)

def populate_layer(resolved: list, config: dict):
        container = Container()
        for provided_cls in resolved:
            setattr(container, provided_cls.name(), providers.Container(provided_cls))

        layer = containers.DynamicContainer()
        layer.config = providers.Configuration()

        for provided_cls in resolved:
            print(f"Resolved class: {provided_cls}")
            setattr(layer, provided_cls.name(), providers.Container(provided_cls, config=layer.config))

        container.override(layer)
        container.config.from_dict(config)
        inject_layer(container)

def inject_layer(container: containers.Container):
    container.check_dependencies()

    for provider in container.traverse(types=[providers.Container]):
            if provider.last_overriding:
                provider.inject(container) # type: ignore