from typing import Any, Union, TypeVar
from dependency_injector import providers

_PROVIDERS = (
    providers.BaseSingleton,
    providers.Factory,
    providers.Resource,
)

T = TypeVar('T', bound=Any)
InstanceOrClass = Union[T, type[T]]

def standalone_provider(cls: T,
    provider: type[providers.Provider[T]]
) -> providers.Provider[T]:
    """Validate standalone provider and return an instance.

    Args:
        cls (type): Instance class to be provided.
        provider (type[providers.Provider[Any]]): Provider class to validate.

    Raises:
        TypeError: If the provider is not a valid type.

    Returns:
        providers.Provider[Any]: Instance of the validated provider.
    """
    if not issubclass(provider, _PROVIDERS):
        raise TypeError(f"Product {cls.__name__} has an invalid provider {provider.__name__} (allowed: {[p.__name__ for p in _PROVIDERS]})") # pragma: no cover
    return provider(cls)

# TODO: validate provider for instance, what about other kinds of providers?
def validate_provider(cls: T,
    provider: InstanceOrClass[providers.Provider[T]]
) -> providers.Provider[T]:
    """Validate provider and return an instance.

    Args:
        cls (Any): Instance class to be provided.
        provider (InstanceOrClass[providers.Provider[Any]]): Provider to validate.

    Raises:
        TypeError: If the provider is not a valid type.

    Returns:
        providers.Provider[Any]: Instance of the validated provider.
    """
    if isinstance(provider, type):
        return standalone_provider(cls, provider)
    else:
        return provider
