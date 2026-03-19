from typing import Any, Callable, Iterable
from dependency_injector import providers
from dependency.core.declaration.component import COMPONENT, Component
from dependency.core.declaration.validation import standalone_provider
from dependency.core.injection.mixin import ProviderMixin

def instance(
    imports: Iterable[type[ProviderMixin]] = (),
    provider: type[providers.Provider[Any]] = providers.Singleton,
    partial_resolution: bool = False,
    strict_resolution: bool = True,
    bootstrap: bool = False,
) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
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
    def wrap(cls: type[COMPONENT]) -> type[COMPONENT]:
        """Register the instance class as the implementation of its parent Component.

        Validates that the class inherits from a Component, creates the provider,
        and registers the declared imports and resolution flags on the Injectable.
        The instance takes ownership of the parent component's Injectable, replacing
        any previously assigned implementation (with a warning if one existed).
        """
        if not issubclass(cls, Component):
            raise TypeError(f"Class {cls} has decorator @instance but is not a subclass of Component") # pragma: no cover

        cls.init_implementation(
            modules_cls=(cls,),
            provider=standalone_provider(cls, provider),
            bootstrap=cls.provide if bootstrap else None,
        )

        cls.update_dependencies(
            imports=imports,
            partial_resolution=partial_resolution,
            strict_resolution=strict_resolution,
        )

        return cls
    return wrap
