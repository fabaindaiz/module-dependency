from typing import Any, Callable, Iterable, Optional, TypeVar
from dependency_injector import providers
from dependency.core.agrupation.module import Module
from dependency.core.declaration.validation import InstanceOrClass, validate_provider
from dependency.core.injection.mixin import ProviderMixin

COMPONENT = TypeVar('COMPONENT', bound='Component')

class Component(ProviderMixin):
    """Base class for all interface declarations in the injection framework.

    A Component defines the interface (contract) that consumers depend on.
    It does not provide any implementation on its own — an Instance must be
    declared to implement it before it can be resolved and provided.

    Components must be decorated with @component to be registered in the
    injection tree. The @component decorator initializes the ProviderInjection
    and Injectable, making the class available as a dependency for other providers.
    """

def component(
    module: Optional[type[Module]] = None,
    imports: Iterable[type[ProviderMixin]] = (),
    partial_resolution: bool = False,
    strict_resolution: bool = True,
    provider: Optional[InstanceOrClass[providers.Provider[Any]]] = None,
    bootstrap: bool = False,
) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
    """Register a Component class as an interface declaration in the injection tree.

    Initializes a ProviderInjection node for the decorated class and registers it
    under the given module. Optionally assigns an inline provider, making the
    component self-providing without requiring a separate @instance declaration.

    The decorated class must be a subclass of Component.

    Args:
        module (type[Module], optional): Module or Plugin this component belongs to.
            If None, the component is registered as an orphan and will be adopted
            by the FallbackPlugin at initialization time. Defaults to None.
        imports (Iterable[type[ProviderMixin]], optional): Components this component
            depends on. Must be declared for all dependencies used in the
            implementation to ensure correct resolution order. Defaults to ().
        provider (InstanceOrClass[providers.Provider], optional): Provider instance
            or class to assign directly to this component, making it self-providing
            without a separate @instance. Accepts Singleton, Factory, or Resource.
            Defaults to None.
        partial_resolution (bool, optional): If True, imports that are outside the
            current provider set are not required to be resolved. Use for components
            that depend on optional or externally-provided dependencies.
            Defaults to False.
        strict_resolution (bool, optional): If False, resolution proceeds even when
            no implementation has been assigned to this component. Use for optional
            interface declarations that may or may not have a concrete implementation.
            Defaults to True.
        bootstrap (bool, optional): If True, the provider is eagerly instantiated
            during the initialization phase by calling .provide() after wiring.
            Defaults to False.

    Raises:
        TypeError: If the decorated class is not a subclass of Component.

    Returns:
        Callable[[type[COMPONENT]], type[COMPONENT]]: Decorator that registers the
            component class and returns it unchanged.
    """
    def wrap(cls: type[COMPONENT]) -> type[COMPONENT]:
        """Register the component class into the injection tree.

        Initializes the ProviderInjection for the class, optionally sets an
        inline provider if one was supplied to the decorator, and registers
        the declared imports and resolution flags on the Injectable.
        """
        if not issubclass(cls, Component):
            raise TypeError(f"Class {cls} has decorator @component but is not a subclass of Component") # pragma: no cover

        cls.init_injection(
            parent=module.injection if module else None
        )

        if provider is not None:
            cls.init_implementation(
                modules_cls=(cls,),
                provider=validate_provider(cls, provider),
                bootstrap=cls.provide if bootstrap else None,
            )

        cls.update_dependencies(
            imports=imports,
            partial_resolution=partial_resolution,
            strict_resolution=strict_resolution,
        )

        return cls
    return wrap
