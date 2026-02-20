from typing import Any, Callable, Iterable, Optional, TypeVar
from dependency_injector import providers
from dependency.core.agrupation.module import Module
from dependency.core.declaration.validation import InstanceOrClass, validate_provider
from dependency.core.injection.mixin import ProviderMixin

COMPONENT = TypeVar('COMPONENT', bound='Component')

class Component(ProviderMixin):
    """Component Base Class
    """

def component(
    module: Optional[type[Module]] = None,
    imports: Iterable[type[ProviderMixin]] = (),
    partial_resolution: bool = False,
    provider: Optional[InstanceOrClass[providers.Provider[Any]]] = None,
    bootstrap: bool = False,
) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
    """Decorator for Component class

    Args:
        module (type[Module], optional): Module where the component is registered. Defaults to None.
        imports (Iterable[type[ProviderMixin]], optional): List of components to be imported by the provider. Defaults to ().
        provider (Optional[providers.Provider[Any]], optional): Provider to be used. Defaults to None.
        partial_resolution (bool, optional): Whether the component should be resolved with partial resolution. Defaults to False.
        bootstrap (bool, optional): Whether the provider should be bootstrapped. Defaults to False.

    Raises:
        TypeError: If the wrapped class is not a subclass of Component.

    Returns:
        Callable[[type[COMPONENT]], COMPONENT]: Decorator function that wraps the component class.
    """
    def wrap(cls: type[COMPONENT]) -> type[COMPONENT]:
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
        )

        return cls
    return wrap
