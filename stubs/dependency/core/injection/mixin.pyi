from dependency.core.exceptions import DeclarationError as DeclarationError
from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection
from dependency.core.injection.wiring import WiringMixin as WiringMixin
from dependency.core.resolution.container import Container as Container
from dependency_injector import containers as containers, providers as providers
from typing import Any, Callable, Generator, Iterable

class ContainerMixin:
    """Mixin for structural units in the injection tree (Module, Plugin).

    Attributes:
        injection (ContainerInjection): The injection node for this container.
    """
    injection: ContainerInjection
    @classmethod
    def on_declaration(cls) -> None:
        """Hook called when the @module decorator is applied."""
    @classmethod
    def on_resolution(cls, container: Container) -> None:
        """Hook called when this module is attached to the application container."""
    @classmethod
    def init_injection(cls, parent: ContainerInjection | None) -> None: ...
    @classmethod
    def change_parent(cls, parent: ContainerMixin | None = None) -> None: ...
    @classmethod
    def inject_container(cls, container: Container) -> None:
        """Attach this module's DynamicContainer to the application container."""
    @classmethod
    def resolve_providers(cls, container: containers.Container | None = None) -> None:
        """Recursively attach child nodes to the DI container tree."""
    @classmethod
    def collect_providers(cls) -> Generator[ProviderInjection, None, None]:
        """Yield all ProviderInjection nodes registered under this container."""

class ProviderMixin(WiringMixin):
    """Mixin for providable units in the injection tree (Component, Product).

    Attributes:
        injection (ProviderInjection): The injection node (tree position + dep tracking).
        injectable (Injectable): The implementation binding (interface -> concrete class).
    """
    injection: ProviderInjection
    injectable: Injectable
    @classmethod
    def on_declaration(cls) -> None:
        """Hook called when the @component/@product decorator is applied."""
    @classmethod
    def init_injection(cls, parent: ContainerInjection | None) -> None: ...
    @classmethod
    def init_implementation(cls, modules_cls: Iterable[type], provider: providers.Provider[Any], bootstrap: Callable[[], Any] | None) -> None:
        """Assign a concrete implementation and DI provider to this component.

        Raises:
            TypeError: If the class is not a subclass of the interface.
        """
    @classmethod
    def change_parent(cls, parent: type['ContainerMixin'] | None = None) -> None: ...
    @classmethod
    def update_dependencies(cls, imports: Iterable[type['ProviderMixin']] = (), optional: Iterable[type['ProviderMixin']] = (), strict_resolution: bool | None = None) -> None:
        """Register required and optional imports, update resolution flags."""
    @classmethod
    def discard_dependencies(cls, imports: Iterable[type['ProviderMixin']] = (), optional: Iterable[type['ProviderMixin']] = ()) -> None:
        """Remove required and optional imports from this provider."""
    @classmethod
    def reference(cls) -> str:
        """Return the dot-separated wiring reference for this provider."""
    @classmethod
    def provider(cls) -> providers.Provider[Any]:
        """Return the dependency-injector provider instance."""
    @classmethod
    def provide(cls, *args: Any, **kwargs: Any) -> Any:
        """Provide an instance of this component."""
