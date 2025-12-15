from typing import Callable, Optional, TypeVar, cast
from dependency.core2.agrupation.base import ABCModule
from dependency.core2.injection.base import ContainerInjection

MODULE = TypeVar('MODULE', bound='Module')

class Module(ABCModule):
    """Module Base Class
    """
    def __init__(self, name: str, injection: ContainerInjection) -> None:
        super().__init__(name)
        self.__injection: ContainerInjection = injection

    @property
    def injection(self) -> ContainerInjection:
        """Get the container injection for the module.

        Returns:
            ContainerInjection: The container injection for the module.
        """
        return self.__injection

def module(
    module: Optional[Module] = None
    ) -> Callable[[type[MODULE]], MODULE]:

    def wrap(cls: type[MODULE]) -> MODULE:
        if not issubclass(cls, Module):
            raise TypeError(f"Class {cls} is not a subclass of Module")

        injection = ContainerInjection(
            name=cls.__name__,
            parent=module.injection if module else None)

        return cls(
            name=cls.__name__,
            injection=injection)
    return wrap
