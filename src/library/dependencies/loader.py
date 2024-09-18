from pprint import pformat
from dependency_injector import containers, providers
from src.library.dependencies.container import ServiceContainer
from src.library.dependencies.resolver import resolve_dependency_layers

class Container(containers.DynamicContainer):
    config: providers.Configuration = providers.Configuration()

def resolve_dependency(container: containers.Container, unresolved_layers: list):
    print("Resolving dependencies")
    resolved_layers = resolve_dependency_layers(unresolved_layers)

    named_layers = pformat([[provider.__name__ for provider in layer] for layer in resolved_layers])
    print(f"Layers:\n{named_layers}")

    for resolved_layer in resolved_layers:
        populate_container(container, resolved_layer)
    
    container.check_dependencies()
    container.init_resources()
    print("Dependencies resolved and injected")

def populate_container(container: containers.Container, resolved_layer: list[ServiceContainer]):
    for provided_cls in resolved_layer:
        setattr(container, provided_cls.name(), providers.Container(provided_cls, config=container.config)) # type: ignore
        provided_cls.inject(container)