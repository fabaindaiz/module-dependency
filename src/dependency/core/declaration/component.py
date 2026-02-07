import logging
from typing import Any, Callable, Iterable, Optional, Union, TypeVar
from dependency_injector import providers
from dependency.core.agrupation.module import Module
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.injection import ProviderInjection
from dependency.core.injection.mixin import ProviderMixin
_logger = logging.getLogger("dependency.loader")

_PROVIDERS = (
    providers.BaseSingleton,
    providers.Factory,
    providers.Resource,
)

COMPONENT = TypeVar('COMPONENT', bound='Component')

class Component(ProviderMixin):
    """Component Base Class
    """

def component(
    module: Optional[type[Module]] = None,
    imports: Iterable[type[ProviderMixin]] = (),
    products: Iterable[type[ProviderMixin]] = (),
    provider: Optional[Union[
        providers.Provider[Any],
        type[providers.Provider[Any]],
    ]] = None,
    bootstrap: bool = False,
) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
    """Decorator for Component class

    Args:
        module (type[Module], optional): Module where the component is registered. Defaults to None.
        imports (Iterable[type[ProviderMixin]], optional): List of components to be imported by the provider. Defaults to ().
        products (Iterable[type[ProviderMixin]], optional): List of products to be declared by the provider. Defaults to ().
        provider (Optional[providers.Provider[Any]], optional): Provider to be used. Defaults to None.
        bootstrap (bool, optional): Whether the provider should be bootstrapped. Defaults to False.

    Raises:
        TypeError: If the wrapped class is not a subclass of Component.

    Returns:
        Callable[[type[COMPONENT]], COMPONENT]: Decorator function that wraps the component class.
    """
    def wrap(cls: type[COMPONENT]) -> type[COMPONENT]:
        if not issubclass(cls, Component):
            raise TypeError(f"Class {cls} has decorator @component but is not a subclass of Component")

        if module is None:
            _logger.warning(f"Component {cls.__name__} has no parent module (consider registering)")

        cls.injection = ProviderInjection(
            name=cls.__name__,
            interface_cls=cls,
            parent=module.injection if module else None,
        )

        if provider is not None:
            _produces: list[type[ProviderMixin]] = list(products)
            _provider: providers.Provider[Any]

            if isinstance(provider, type):
                if not issubclass(provider, _PROVIDERS):
                    raise TypeError(f"Product {cls.__name__} has an invalid provider {provider.__name__} (allowed: {[p.__name__ for p in _PROVIDERS]})")
                _provider = provider(cls)

            else:
                if len(_produces) == 0:
                    _logger.warning(f"Component {cls.__name__} has a provider but no provided classes")
                _provider = provider

            cls.injection.set_instance(
                injectable = Injectable(
                    component_cls=cls,
                    provided_cls=_produces,
                    provider=_provider,
                    imports=(
                        provider.injection.injectable
                        for provider in imports
                    ),
                    products=(
                        provider.injection.injectable
                        for provider in products
                    ),
                    bootstrap=cls.provide if bootstrap else None,
                )
            )

        return cls
    return wrap
