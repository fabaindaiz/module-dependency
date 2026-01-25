from dependency.core.exceptions import DeclarationError as DeclarationError
from dependency.core.injection.base import BaseInjection as BaseInjection, ContainerInjection as ContainerInjection
from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.wiring import LazyProvide as LazyProvide
from dependency_injector import providers as providers
from typing import Any, Generator, override

class ProviderMixin:
    """Component Base Class

    Attributes:
        injection (ProviderInjection): Injection handler for the component
        interface_cls (type): Interface class for the component
    """
    injection: ProviderInjection
    interface_cls: type
    @classmethod
    def reference(cls) -> str:
        """Return the reference name of the component."""
    @classmethod
    def provider(cls) -> providers.Provider[Any]:
        """Return the provider instance of the component."""
    @classmethod
    def provide(cls, *args: Any, **kwargs: Any) -> Any:
        """Provide an instance of the interface class"""

class ProviderInjection(BaseInjection):
    """Provider Injection Class
    """
    interface_cls: type
    def __init__(self, name: str, interface_cls: type, parent: ContainerInjection | None = None) -> None: ...
    @property
    def provider(self) -> providers.Provider[Any]:
        """Return the provider instance."""
    @property
    def injectable(self) -> Injectable:
        """Return the injectable instance."""
    def set_instance(self, injectable: Injectable) -> None:
        """Set the injectable instance and its imports."""
    @override
    def inject_cls(self) -> providers.Provider[Any]:
        """Return the provider instance."""
    @override
    def resolve_providers(self) -> Generator[Injectable, None, None]:
        """Inject all imports into the current injectable."""
