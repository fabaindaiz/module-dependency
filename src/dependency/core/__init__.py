from dependency.core.agrupation import (
    Entrypoint,
    Module,
    module,
    Plugin,
    PluginMeta,
)
from dependency.core.declaration import (
    Component,
    component,
    Instance,
    instance,
    providers,
)
from dependency.core.resolution import (
    Container,
    InjectionResolver,
)
from dependency.core.exceptions import (
    DependencyError,
)

__all__ = [
    "Entrypoint",
    "Module",
    "module",
    "Plugin",
    "PluginMeta",
    "Component",
    "component",
    "Instance",
    "instance",
    "providers",
    "Container",
    "InjectionResolver",
    "DependencyError",
]

# TODO: Simplificar los imports utilizados para definir una aplicación
