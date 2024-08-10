from dependency_injector import containers, providers
from src.container import Container

def resolve_dependencies(unresolved_layers):
    resolved_layers = []

    # Mientras haya dependencias no resueltas
    while unresolved_layers:
        new_layer = []

        # Recorremos todas las dependencias no resueltas
        for provider in unresolved_layers:
            # Obtenemos las dependencias de la clase
            dependencies = provider.depends()

            # Verificamos si todas las dependencias están resueltas
            if all(
                any(
                    issubclass(dep, res)
                    for res in resolved
                )
                for dep in dependencies
                for resolved in resolved_layers
            ):
                # Si están resueltas, añadimos la clase a la nueva capa
                new_layer.append(provider)

        # Si no se ha podido resolver ninguna nueva dependencia, significa que hay un ciclo
        if not new_layer:
            raise ValueError("No se pueden resolver las dependencias, puede haber un ciclo")

        # Añadimos la nueva capa a la lista de capas resueltas
        resolved_layers.append(new_layer)

        # Quitamos las clases resueltas de la lista de dependencias no resueltas
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