from dependency_injector import containers, providers
from src.dependencies.container import ServiceContainer
from src.dependencies.resolver import resolve_dependency_layers

class Container(containers.DynamicContainer):
    config: providers.Configuration = providers.Configuration()

def resolve_dependency(container: containers.Container, unresolved_layers: list):
    for resolved_layer in resolve_dependency_layers(unresolved_layers):
        populate_container(container, resolved_layer)

def populate_container(container: containers.Container, resolved_layer: list[ServiceContainer]):
    for provided_cls in resolved_layer:
        setattr(container, provided_cls.name(), providers.Container(provided_cls, config=container.config))
        provided_cls.inject(container)