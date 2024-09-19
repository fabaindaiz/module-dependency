from pprint import pformat
from core import Module
from core.resolver import resolve_dependency_layers
from dependency_injector import containers, providers

class Container(containers.DynamicContainer):
    config: providers.Configuration = providers.Configuration()

def resolve_dependency(container: containers.Container, module: Module):
    print("Resolving dependencies")

    unresolved_layers = module.dependencies()
    resolved_layers = resolve_dependency_layers(unresolved_layers)

    named_layers = pformat([[provider._name for provider in layer] for layer in resolved_layers])
    print(f"Layers:\n{named_layers}")

    for resolved_layer in resolved_layers:
        populate_container(container, resolved_layer)
    
    container.check_dependencies()
    container.init_resources()
    print("Dependencies resolved and injected")

def populate_container(container: containers.Container, resolved_layer: list):
    for provided_cls in resolved_layer:
        setattr(container, provided_cls._component._name, providers.Container(provided_cls._container, _config=container.config)) # type: ignore
        provided_cls._component.wire(container)