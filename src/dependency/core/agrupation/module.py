from typing import Callable, Optional, TypeVar
from dependency.core.injection.mixin import ContainerMixin

MODULE = TypeVar('MODULE', bound='Module')

class Module(ContainerMixin):
    """Module Base Class
    """

def module(
    module: Optional[type[Module]] = None
) -> Callable[[type[MODULE]], type[MODULE]]:
    """Decorator for Module class

    Args:
        module (type[Module], optional): Parent module class which this module belongs to. Defaults to None.

    Raises:
        TypeError: If the wrapped class is not a subclass of Module.

    Returns:
        Callable[[type[MODULE]], MODULE]: Decorator function that wraps the module class.
    """
    def wrap(cls: type[MODULE]) -> type[MODULE]:
        if not issubclass(cls, Module):
            raise TypeError(f"Class {cls} has decorator @module but is not a subclass of Module")

        cls.init_injection(
            parent=module.injection if module else None
        )

        return cls
    return wrap
