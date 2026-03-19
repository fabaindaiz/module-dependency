from dependency.core.declaration.component import COMPONENT as COMPONENT, Component as Component
from dependency.core.declaration.validation import standalone_provider as standalone_provider
from dependency.core.injection.mixin import ProviderMixin as ProviderMixin
from dependency_injector import providers
from typing import Any, Callable, Iterable

def instance(imports: Iterable[type[ProviderMixin]] = (), provider: type[providers.Provider[Any]] = ..., partial_resolution: bool = False, strict_resolution: bool = True, bootstrap: bool = False) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
    """Register a class as the concrete implementation of a Component.

    Takes ownership of the parent Component's Injectable by calling
    init_implementation, which assigns this class as the implementation and
    creates the provider. If another @instance was already applied to the
    same Component, a warning is logged and this one replaces it.

    The decorated class must be a subclass of the Component it implements.

    Args:
        imports (Iterable[type[ProviderMixin]], optional): Components this instance
            depends on. Must be declared for all dependencies used in __init__ or
            injected methods to ensure correct resolution order. Defaults to ().
        provider (type[providers.Provider], optional): Provider class to use.
            Accepts Singleton, Factory, or Resource. Defaults to providers.Singleton.
        partial_resolution (bool, optional): If True, imports that are outside the
            current provider set are not required to be resolved. Use for instances
            that depend on optional or externally-provided dependencies.
            Defaults to False.
        strict_resolution (bool, optional): If False, resolution proceeds even when
            this instance has no implementation assigned. Rarely needed on @instance
            since the decorated class itself is the implementation. Defaults to True.
        bootstrap (bool, optional): If True, the provider is eagerly instantiated
            during the initialization phase by calling .provide() after wiring,
            triggering __init__ immediately at startup. Defaults to False.

    Raises:
        TypeError: If the decorated class is not a subclass of its parent Component.

    Returns:
        Callable[[type[COMPONENT]], type[COMPONENT]]: Decorator that registers the
            instance class and returns it unchanged.
    """
