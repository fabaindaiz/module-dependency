from typing import Callable, Iterable, Optional, TypeVar
from dependency.core.injection.mixin import ContainerMixin, ProviderMixin

MODULE = TypeVar('MODULE', bound='Module')

class Module(ContainerMixin):
    """Base class for all structural grouping units in the framework.

    A Module organizes related Components and Products under a common namespace
    within the injection tree. It carries no logic of its own — its only role is
    structural: to define scope and hierarchy for the providers registered under it.

    Modules must be decorated with @module to be registered in the injection tree.
    """

def module(
    module: Optional[type[Module]] = None,
    provides: Iterable[type[ProviderMixin]] = (),
) -> Callable[[type[MODULE]], type[MODULE]]:
    """Register a Module class into the injection tree.

    Initializes a ContainerInjection node for the decorated class and attaches
    it to the parent module's injection node if one is provided. The decorated
    class must be a subclass of Module.

    Args:
        module (type[Module], optional): Parent module or plugin this module
            belongs to. If None, the module is registered without a parent —
            it will be treated as an orphan unless it is itself a Plugin root.
            Defaults to None.
        provides (Iterable[type[ProviderMixin]], optional): Providers to assign
            to this module. Alternative to declaring module= on each provider.
            Defaults to ().

    Raises:
        TypeError: If the decorated class is not a subclass of Module.

    Returns:
        Callable[[type[MODULE]], type[MODULE]]: Decorator that registers the
            module class and returns it unchanged.
    """
    def wrap(cls: type[MODULE]) -> type[MODULE]:
        if not issubclass(cls, Module):
            raise TypeError(f"Class {cls} has decorator @module but is not a subclass of Module") # pragma: no cover

        cls.init_injection(
            parent=module.injection if module else None
        )

        for provider in provides:
            provider.change_parent(cls)

        return cls
    return wrap
