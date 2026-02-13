from dependency_injector import providers
from typing import Any, TypeVar

T = TypeVar('T', bound=Any)
InstanceOrClass = T | type[T]

def standalone_provider(cls, provider: type[providers.Provider[T]]) -> providers.Provider[T]:
    """Validate standalone provider and return an instance.

    Args:
        cls (type): Instance class to be provided.
        provider (type[providers.Provider[Any]]): Provider class to validate.

    Raises:
        TypeError: If the provider is not a valid type.

    Returns:
        providers.Provider[Any]: Instance of the validated provider.
    """
def validate_provider(cls, provider: InstanceOrClass[providers.Provider[T]]) -> providers.Provider[T]:
    """Validate provider and return an instance.

    Args:
        cls (Any): Instance class to be provided.
        provider (InstanceOrClass[providers.Provider[Any]]): Provider to validate.

    Raises:
        TypeError: If the provider is not a valid type.

    Returns:
        providers.Provider[Any]: Instance of the validated provider.
    """
