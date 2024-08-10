from dependency_injector import containers, providers
from src.dependencies.resolver import resolve_dependency_layers

class Container(containers.DynamicContainer):
    config: providers.Configuration = providers.Dependency()

def load_dependencies(unresolved: list, config: dict):
    container = Container()

    for provider in unresolved:
        setattr(container, provider.name(), providers.Container(provider))

    for resolved_layer in resolve_dependency_layers(unresolved):
        populate_layer(container, resolved_layer, config)

def populate_layer(container: Container, resolved: list, config: dict):
        layer = containers.DynamicContainer()
        layer.config = providers.Configuration()

        for provided_cls in resolved:
            setattr(layer, provided_cls.name(), providers.Container(provided_cls, config=layer.config))

        container.override(layer)
        container.config.from_dict(config)
        inject_layer(container)

def inject_layer(container: containers.Container):
    container.check_dependencies()

    for provider in container.traverse(types=[providers.Container]):
            if provider.last_overriding:
                provider.inject(container) # type: ignore