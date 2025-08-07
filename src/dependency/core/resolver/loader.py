from pprint import pformat
from typing import cast
from dependency.core.agrupation.module import Module
from dependency.core.injection.container import Container

def resolve_dependency(container: Container, appmodule: type[Module]) -> None:
    # Cast due to mypy not supporting class decorators
    _appmodule = cast(Module, appmodule)
    print(f"Resolving dependencies in {_appmodule}")

    unresolved_layers = _appmodule.init_providers()
    resolved_layers = resolve_dependency_layers(unresolved_layers)

    named_layers = pformat(resolved_layers)
    print(f"Resolved layers:\n{named_layers}")

    for resolved_layer in resolved_layers:
        for provider in resolved_layer:
            provider.resolve(container, unresolved_layers, config=container.config)
    
    container.check_dependencies()
    container.init_resources()
    _appmodule.init_modules(unresolved_layers)
    _appmodule.init_bootstrap()
    print("Dependencies resolved and injected")