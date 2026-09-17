from typing import Any, Union, TypeVar
from dependency_injector import providers

_PROVIDERS = (
    providers.BaseSingleton,
    providers.Factory,
    providers.Resource,
)

T = TypeVar('T', bound=Any)
InstanceOrClass = Union[T, type[T]]

def standalone_provider(
    provided_cls: type[T],
    provider: type[providers.Provider[T]],
) -> providers.Provider[T]:
    """Validate standalone provider and return an instance.

    Args:
        provided_cls (type[T]): Class whose instances the provider will build.
        provider (type[providers.Provider[Any]]): Provider class to validate.

    Raises:
        TypeError: If the provider is not a valid type.

    Returns:
        providers.Provider[Any]: Instance of the validated provider.
    """
    if not issubclass(provider, _PROVIDERS):
        raise TypeError(f"Product {provided_cls.__name__} has an invalid provider {provider.__name__} (allowed: {[p.__name__ for p in _PROVIDERS]})") # pragma: no cover
    return provider(provided_cls)

# TODO: validate provider for instance, what about other kinds of providers?
def validate_provider(
    provided_cls: type[T],
    provider: InstanceOrClass[providers.Provider[T]],
) -> providers.Provider[T]:
    """Validate provider and return an instance.

    Args:
        provided_cls (type[T]): Class whose instances the provider will build.
        provider (InstanceOrClass[providers.Provider[Any]]): Provider to validate.

    Raises:
        TypeError: If the provider is not a valid type.

    Returns:
        providers.Provider[Any]: Instance of the validated provider.
    """
    if isinstance(provider, type):
        return standalone_provider(provided_cls, provider)
    else:
        return provider
