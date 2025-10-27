from dependency.core.agrupation.module import Module as Module
from dependency.core.declaration.base import ABCComponent as ABCComponent, ABCInstance as ABCInstance
from dependency.core.exceptions import DependencyError as DependencyError
from dependency.core.injection.base import ProviderInjection as ProviderInjection
from typing import Any, Callable, TypeVar

COMPONENT = TypeVar('COMPONENT', bound='Component')

class Component(ABCComponent):
    """Component Base Class
    """
    def __init__(self, interface_cls: type, injection: ProviderInjection) -> None: ...
    @property
    def reference(self) -> str:
        """Get the injection reference for the component.

        Returns:
            str: The injection reference for the component.
        """
    @property
    def injection(self) -> ProviderInjection:
        """Get the provider injection for the component.

        Returns:
            ProviderInjection: The provider injection for the component.
        """
    @property
    def instance(self) -> ABCInstance | None:
        """Get the instance for the component.

        Returns:
            Optional[ABCInstance]: The instance for the component, if it exists.
        """
    @instance.setter
    def instance(self, instance: ABCInstance) -> None:
        """Set the instance for the component.

        Args:
            instance (ABCInstance): The instance to set for the component.

        Raises:
            DependencyError: If the component is already instanced.
        """
    @staticmethod
    def provide() -> Any:
        """Provide the component instance.

        Returns:
            Any: The component instance.
        """

def component(module: type[Module], interface: type) -> Callable[[type[COMPONENT]], COMPONENT]:
    """Decorator for Component class

    Args:
        module (ABCModule): Module instance to register the component.
        interface (type): Interface class to be used as a base class for the component.
    
    Raises:
        TypeError: If the wrapped class is not a subclass of Component.

    Returns:
        Callable[[type[Component]], Component]: Decorator function that wraps the component class.
    """
