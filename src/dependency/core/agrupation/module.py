import logging
from typing import Callable, Optional, TypeVar
from dependency.core.injection.base import ContainerInjection
from dependency.core.injection.injectable import Injectable
from dependency.core.resolution.container import Container
_logger = logging.getLogger("DependencyLoader")

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
        setattr(container, cls.injection.name, cls.injection.inject_cls())

    @classmethod
    def resolve_providers(cls) -> list[Injectable]:
        """Resolve provider injections for the plugin.

        Returns:
            list[Injectable]: A list of injectable providers.
        """
        return [provider for provider in cls.injection.resolve_providers()]

def module(
    module: Optional[type[Module]] = None
) -> Callable[[type[MODULE]], type[MODULE]]:
    """Decorator for Module class

    Args:
        module (Optional[Module]): Parent module class which this module belongs to.

    Raises:
        TypeError: If the wrapped class is not a subclass of Module.

    Returns:
        Callable[[type[MODULE]], MODULE]: Decorator function that wraps the module class.
    """
    def wrap(cls: type[MODULE]) -> type[MODULE]:
        if not issubclass(cls, Module):
            raise TypeError(f"Class {cls} is not a subclass of Module")

        injection = ContainerInjection(
            name=cls.__name__,
            parent=module.injection if module else None,
        )
        cls.injection = injection

        return cls
    return wrap
