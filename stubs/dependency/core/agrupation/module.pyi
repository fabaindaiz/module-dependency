from dependency.core.agrupation.base import ABCModule as ABCModule
from dependency.core.injection.base import ContainerInjection as ContainerInjection
from typing import Callable, TypeVar

MODULE = TypeVar('MODULE', bound='Module')

class Module(ABCModule):
    """Module Base Class
    """
    def __init__(self, name: str, injection: ContainerInjection) -> None: ...
    @property
    def injection(self) -> ContainerInjection:
        """Get the container injection for the module.

        Returns:
            ContainerInjection: The container injection for the module.
        """

def module(module: Module | None = None) -> Callable[[type[MODULE]], MODULE]:
    """Decorator for Module class

    Args:
        module (Optional[type[Module]]): Parent module class which this module belongs to.

    Returns:
        Callable[[type[Module]], Module]: Decorator function that wraps the module class.
    """
