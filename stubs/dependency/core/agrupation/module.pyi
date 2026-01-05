from dependency.core.injection.base import ContainerInjection as ContainerInjection
from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.resolution.container import Container as Container
from typing import Callable, TypeVar

MODULE = TypeVar('MODULE', bound='Module')

class Module:
    """Module Base Class
    """
    injection: ContainerInjection
    @classmethod
    def inject_container(cls, container: Container) -> None:
        """Inject the module into the application container.

        Args:
            container (Container): The application container.
        """
    @classmethod
    def resolve_providers(cls) -> list[Injectable]:
        """Resolve provider injections for the plugin.

        Returns:
            list[Injectable]: A list of injectable providers.
        """

def module(module: type[Module] | None = None) -> Callable[[type[MODULE]], type[MODULE]]:
    """Decorator for Module class

    Args:
        module (Optional[Module]): Parent module class which this module belongs to.

    Raises:
        TypeError: If the wrapped class is not a subclass of Module.

    Returns:
        Callable[[type[MODULE]], MODULE]: Decorator function that wraps the module class.
    """
