from dependency_injector import providers
from typing import Any, TypeVar

T = TypeVar('T', bound=Any)
InstanceOrClass = T | type[T]

def standalone_provider(provided_cls: type[T], provider: type[providers.Provider[T]]) -> providers.Provider[T]:
    """Validate standalone provider and return an instance.

    Args:
        provided_cls (type[T]): Class whose instances the provider will build.
        provider (type[providers.Provider[Any]]): Provider class to validate.

    Raises:
        TypeError: If the provider is not a valid type.

    Returns:
        providers.Provider[Any]: Instance of the validated provider.
    """
def validate_provider(provided_cls: type[T], provider: InstanceOrClass[providers.Provider[T]]) -> providers.Provider[T]:
    """Validate provider and return an instance.

    Args:
        provided_cls (type[T]): Class whose instances the provider will build.
        provider (InstanceOrClass[providers.Provider[Any]]): Provider to validate.

    Raises:
        TypeError: If the provider is not a valid type.

    Returns:
        providers.Provider[Any]: Instance of the validated provider.
    """
