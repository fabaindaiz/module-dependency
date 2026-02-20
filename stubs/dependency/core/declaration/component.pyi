from dependency.core.agrupation.module import Module as Module
from dependency.core.declaration.validation import InstanceOrClass as InstanceOrClass, validate_provider as validate_provider
from dependency.core.injection.mixin import ProviderMixin as ProviderMixin
from dependency_injector import providers as providers
from typing import Any, Callable, Iterable, TypeVar

COMPONENT = TypeVar('COMPONENT', bound='Component')

class Component(ProviderMixin):
    """Component Base Class
    """

def component(module: type[Module] | None = None, imports: Iterable[type[ProviderMixin]] = (), partial_resolution: bool = False, provider: InstanceOrClass[providers.Provider[Any]] | None = None, bootstrap: bool = False) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
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
