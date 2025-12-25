from typing import Callable, Optional, TypeVar
from dependency.core.agrupation.base import ABCModule
from dependency.core.injection.base import ContainerInjection
from dependency.core.injection.injectable import Injectable
from dependency.core.resolution.container import Container

MODULE = TypeVar('MODULE', bound='Module')

class Module(ABCModule):
    """Module Base Class
    """
    def __init__(self, name: str, injection: ContainerInjection) -> None:
        super().__init__(name)
        self.injection: ContainerInjection = injection

    def inject_container(self, container: Container) -> None:
        """Inject the module into the application container.

        Args:
            container (Container): The application container.
        """
        setattr(container, self.injection.name, self.injection.inject_cls())

    def resolve_providers(self) -> list[Injectable]:
        """Resolve provider injections for the plugin.

        Returns:
            list[Injectable]: A list of injectable providers.
        """
        return [provider for provider in self.injection.resolve_providers()]

def module(
    module: Optional[Module] = None
) -> Callable[[type[MODULE]], MODULE]:
    """Decorator for Module class

    Args:
        module (Optional[Module]): Parent module class which this module belongs to.

    Raises:
        TypeError: If the wrapped class is not a subclass of Module.

    Returns:
        Callable[[type[MODULE]], MODULE]: Decorator function that wraps the module class.
    """
    def wrap(cls: type[MODULE]) -> MODULE:
        if not issubclass(cls, Module):
            raise TypeError(f"Class {cls} is not a subclass of Module")

        injection = ContainerInjection(
            name=cls.__name__,
            parent=module.injection if module else None,
        )

        return cls(
            name=cls.__name__,
            injection=injection,
        )
    return wrap
