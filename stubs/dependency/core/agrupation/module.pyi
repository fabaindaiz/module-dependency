from dependency.core.injection.injection import ContainerInjection as ContainerInjection
from dependency.core.injection.mixin import ContainerMixin as ContainerMixin
from typing import Callable, TypeVar

MODULE = TypeVar('MODULE', bound='Module')

class Module(ContainerMixin):
    """Module Base Class
    """

def module(module: type[Module] | None = None) -> Callable[[type[MODULE]], type[MODULE]]:
    """Decorator for Module class

    Args:
        module (type[Module], optional): Parent module class which this module belongs to. Defaults to None.

    Raises:
        TypeError: If the wrapped class is not a subclass of Module.

    Returns:
        Callable[[type[MODULE]], MODULE]: Decorator function that wraps the module class.
    """
