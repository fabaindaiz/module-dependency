import logging
logger = logging.getLogger("DependencyLoader")

from dependency_injector import containers, providers
from src.dependencies.container import ServiceContainer
from src.dependencies.resolver import resolve_dependency_layers

class Container(containers.DynamicContainer):
    config: providers.Configuration = providers.Configuration()

def resolve_dependency(container: containers.Container, unresolved_layers: list):
    logger.info("Resolving dependencies")
    resolved_layers = resolve_dependency_layers(unresolved_layers)

    for resolved_layer in resolved_layers:
        logger.debug(f"layer: {resolved_layer}")
        populate_container(container, resolved_layer)
    
    container.check_dependencies()
    logger.info("Dependencies resolved and injected")

def populate_container(container: containers.Container, resolved_layer: list[ServiceContainer]):
    for provided_cls in resolved_layer:
        setattr(container, provided_cls.name(), providers.Container(provided_cls, config=container.config))
        provided_cls.inject(container)