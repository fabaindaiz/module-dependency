from typing import Any, Callable, Generator, Iterable, Optional
from dependency_injector import providers, containers
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.injection import ContainerInjection, ProviderInjection
from dependency.core.injection.wiring import WiringMixin
from dependency.core.resolution.container import Container
from dependency.core.exceptions import DeclarationError

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
    def init_injection(cls, parent: Optional[ContainerInjection]) -> None:
        cls.injection = ContainerInjection(
            name=cls.__name__,
            parent=parent,
        )
        cls.on_declaration()

    @classmethod
    def change_parent(cls, parent: Optional['ContainerMixin'] = None) -> None:
        cls.injection.change_parent(parent.injection if parent else None)

    @classmethod
    def inject_container(cls, container: Container) -> None:
        """Attach this module's DynamicContainer to the application container."""
        setattr(container, cls.injection.name, cls.injection.container)
        cls.on_resolution(container=container)

    @classmethod
    def resolve_providers(cls, container: Optional[containers.Container] = None) -> None:
        """Recursively attach child nodes to the DI container tree."""
        cls.injection.attach(container=container)

    @classmethod
    def collect_providers(cls) -> Generator[ProviderInjection, None, None]:
        """Yield all ProviderInjection nodes registered under this container."""
        return cls.injection.collect_providers()

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
    def init_injection(cls,
        parent: Optional[ContainerInjection],
    ) -> None:
        cls.injectable = Injectable(interface_cls=cls)
        cls.injection = ProviderInjection(
            name=cls.__name__,
            injectable=cls.injectable,
            parent=parent,
        )
        cls.on_declaration()

    @classmethod
    def init_implementation(cls,
        modules_cls: Iterable[type],
        provider: providers.Provider[Any],
        bootstrap: Optional[Callable[[], Any]],
    ) -> None:
        """Assign a concrete implementation and DI provider to this component.

        Raises:
            TypeError: If the class is not a subclass of the interface.
        """
        interface_cls: type = cls.injectable.interface_cls
        if not issubclass(cls, interface_cls):
            raise TypeError(f"Class {cls.__name__} must be a subclass of {interface_cls.__name__} to be used as an instance of component {cls.__name__}")

        cls.injection.set_provider(provider=provider)
        cls.injectable.set_implementation(
            implementation=cls,
            modules_cls=modules_cls,
            bootstrap=bootstrap,
        )

    @classmethod
    def change_parent(cls, parent: Optional[type['ContainerMixin']] = None) -> None:
        cls.injection.change_parent(parent.injection if parent else None)

    @classmethod
    def update_dependencies(cls,
        imports: Iterable[type['ProviderMixin']] = (),
        optional: Iterable[type['ProviderMixin']] = (),
        strict_resolution: Optional[bool] = None,
    ) -> None:
        """Register required and optional imports, update resolution flags."""
        cls.injection.update_dependencies(
            imports={provider.injection for provider in imports},
            optional={provider.injection for provider in optional},
            strict_resolution=strict_resolution,
        )

    @classmethod
    def discard_dependencies(cls,
        imports: Iterable[type['ProviderMixin']] = (),
        optional: Iterable[type['ProviderMixin']] = (),
    ) -> None:
        """Remove required and optional imports from this provider."""
        cls.injection.discard_dependencies(
            imports={provider.injection for provider in imports},
            optional={provider.injection for provider in optional},
        )

    @classmethod
    def reference(cls) -> str:
        """Return the dot-separated wiring reference for this provider."""
        return cls.injection.reference

    @classmethod
    def provider(cls) -> providers.Provider[Any]:
        """Return the dependency-injector provider instance."""
        return cls.injection.provider

    @classmethod
    def provide(cls, *args: Any, **kwargs: Any) -> Any:
        """Provide an instance of this component."""
        if not cls.injection.is_resolved:
            raise DeclarationError(
                f"Injectable {cls.injection} accessed before being resolved. "
                f"Ensure it is declared as a dependency where it is being used."
            )
        return cls.injection.provider(*args, **kwargs)
