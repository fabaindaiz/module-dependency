from typing import Callable, cast
from dependency_injector import providers
from dependency.core.declaration.component import Component
from dependency.core.declaration.base import ABCInstance

class Instance(ABCInstance):
    """Instance Base Class
    """
    def __init__(self, provided_cls: type):
        super().__init__(provided_cls=provided_cls)

def instance(
        component: type[Component],
        provider: type[providers.Provider] = providers.Singleton
    ) -> Callable[[type], Instance]:
    """Decorator for instance class

    Args:
        component (type[Component]): Component class to be used as a base class for the provider.
        imports (list[type[Component]], optional): List of components to be imported by the provider. Defaults to [].
        dependents (list[type[Dependent]], optional): List of dependents to be declared by the provider. Defaults to [].
        provider (type[providers.Provider], optional): Provider class to be used. Defaults to providers.Singleton.

    Raises:
        TypeError: If the wrapped class is not a subclass of Component declared base class.

    Returns:
        Callable[[type], Provider]: Decorator function that wraps the provider class.
    """
    # Cast due to mypy not supporting class decorators
    _component = cast(Component, component)
    def wrap(cls: type) -> Instance:
        if not issubclass(cls, _component.interface_cls):
            raise TypeError(f"Class {cls} is not a subclass of {_component.interface_cls}")
        
        instance_wrap = Instance(
            provided_cls=cls
        )
        _component.instance = instance_wrap
        _component.injection.set_instance(provided_cls=cls, provider_cls=provider)
        return instance_wrap
    return wrap