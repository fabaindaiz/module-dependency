from typing import Any, Callable, Iterable
from dependency_injector import providers
from dependency.core.declaration.component import COMPONENT, Component
from dependency.core.declaration.validation import standalone_provider
from dependency.core.injection.mixin import ProviderMixin

def instance(
    imports: Iterable[type[ProviderMixin]] = (),
    provider: type[providers.Provider[Any]] = providers.Singleton,
    partial_resolution: bool = False,
    strict_resolution: bool = True,
    bootstrap: bool = False,
) -> Callable[[type[COMPONENT]], type[COMPONENT]]:
    """Decorator for instance class

    Args:
        imports (Iterable[type[ProviderMixin]], optional): List of components to be imported by the provider. Defaults to ().
        provider (type[providers.Provider[Any]], optional): Provider to be used. Defaults to providers.Singleton.
        partial_resolution (bool, optional): Whether the component should not expand dependencies recursively. Defaults to False.
        strict_resolution (bool, optional): Whether the component should be resolved even if it has no implementation. Defaults to True.
        bootstrap (bool, optional): Whether the provider should be bootstrapped. Defaults to False.

    Raises:
        TypeError: If the wrapped class is not a subclass of Component declared base class.

    Returns:
        Callable[[type[COMPONENT]], COMPONENT]: Decorator function that wraps the instance class.
    """
    def wrap(cls: type[COMPONENT]) -> type[COMPONENT]:
        if not issubclass(cls, Component):
            raise TypeError(f"Class {cls} has decorator @instance but is not a subclass of Component") # pragma: no cover

        cls.init_implementation(
            modules_cls=(cls,),
            provider=standalone_provider(cls, provider),
            bootstrap=cls.provide if bootstrap else None,
        )

        cls.update_dependencies(
            imports=imports,
            partial_resolution=partial_resolution,
            strict_resolution=strict_resolution,
        )

        return cls
    return wrap
