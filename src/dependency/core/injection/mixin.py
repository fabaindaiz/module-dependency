from typing import Any, Callable, Generator, Iterable, Optional
from dependency_injector import providers, containers
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.injection import ContainerInjection, ProviderInjection
from dependency.core.injection.wiring import WiringMixin
from dependency.core.resolution.container import Container
from dependency.core.resolution.registry import Registry
from dependency.core.exceptions import DeclarationError

class ContainerMixin:
    """Mixin class for structural units in the injection tree (Module, Plugin).

    Provides class-level methods to initialize, attach, and resolve a
    ContainerInjection node. All structural classes (Module, Plugin) inherit
    from this mixin to participate in the injection hierarchy.

    Attributes:
        injection (ContainerInjection): The injection node for this container.
    """
    injection: ContainerInjection

    @classmethod
    def on_declaration(cls) -> None:
        """Hook method called upon declaration of the container.
        """

    @classmethod
    def on_resolution(cls, container: Container) -> None:
        """Hook method called upon resolution of the container.

        Args:
            container (Container): The application container.
        """

    @classmethod
    def init_injection(cls, parent: Optional[ContainerInjection]) -> None:
        """Initialize the injection for the container.

        Args:
            parent (Optional[ContainerInjection]): Parent container injection instance.
        """
        cls.injection = ContainerInjection(
            name=cls.__name__,
            parent=parent,
        )
        cls.on_declaration()
        Registry.register_container(cls.injection)

    @classmethod
    def change_parent(cls, parent: Optional['ContainerMixin'] = None) -> None:
        """Change the parent injection of this mixin.

        Args:
            parent (ContainerMixin): The new parent container.
        """
        cls.injection.change_parent(parent.injection if parent else None)

    @classmethod
    def inject_container(cls, container: Container) -> None:
        """Inject the module into the application container.

        Args:
            container (Container): The application container.
        """
        setattr(container, cls.injection.name, cls.injection.container)
        cls.on_resolution(container=container)

    @classmethod
    def resolve_providers(cls, container: Optional[containers.Container] = None) -> None:
        """Resolve all child providers into this container's DynamicContainer.

        Delegates to ContainerInjection.resolve_providers, which recursively
        attaches each child ProviderInjection to the appropriate sub-container.

        Args:
            container (containers.Container, optional): If provided, also attaches
                this container as an attribute of the given parent container.
        """
        cls.injection.resolve_providers(container=container)

    @classmethod
    def resolve_injectables(cls) -> Generator[Injectable, None, None]:
        """Yield all Injectable objects registered under this container.

        Walks the ContainerInjection tree and yields every Injectable found in
        child ProviderInjection nodes. Used during Phase 2 of resolution to
        collect the full set of providers to resolve.

        Returns:
            Generator[Injectable, None, None]: A generator of injectables.
        """
        return cls.injection.resolve_injectables()

class ProviderMixin(WiringMixin):
    """Mixin class for providable units in the injection tree (Component, Product).

    Provides class-level methods to initialize a ProviderInjection node, assign
    an implementation, manage dependencies, and expose the underlying provider.
    All providable classes (Component, Product) inherit from this mixin.

    Attributes:
        injection (ProviderInjection): The injection node for this provider.
        injectable (Injectable): The injectable tracking implementation and imports.
    """
    injection: ProviderInjection
    injectable: Injectable

    @classmethod
    def on_declaration(cls) -> None:
        """Hook method called upon declaration of the provider.
        """

    @classmethod
    def init_injection(cls,
        parent: Optional[ContainerInjection],
    ) -> None:
        """Initialize the injection for the provider.

        Args:
            parent (Optional[ContainerInjection]): Parent container injection instance.
        """
        cls.injectable = Injectable(
            interface_cls=cls
        )
        cls.injection = ProviderInjection(
            name=cls.__name__,
            injectable=cls.injectable,
            parent=parent,
        )
        cls.on_declaration()
        Registry.register_provider(cls.injection)

    @classmethod
    def init_implementation(cls,
        modules_cls: Iterable[type],
        provider: providers.Provider[Any],
        bootstrap: Optional[Callable[[], Any]],
    ) -> None:
        """Initialize the injectable for the provider.

        Args:
            modules_cls (Iterable[type]): List of modules that need to be wired for the provider.
            provider (providers.Provider[Any]): Provider instance to be used for the injectable.
            bootstrap (Optional[Callable[[], Any]]): Whether the provider should be bootstrapped.

        Raises:
            TypeError: If the class is not a subclass of the interface class.
        """
        interface_cls: type = cls.injectable.interface_cls
        if not issubclass(cls, interface_cls):
            raise TypeError(f"Class {cls.__name__} must be a subclass of {interface_cls.__name__} to be used as an instance of component {cls.__name__}")

        cls.injection.set_provider(
            provider=provider
        )
        cls.injectable.set_implementation(
            implementation=cls,
            modules_cls=modules_cls,
            bootstrap=bootstrap,
        )

    @classmethod
    def change_parent(cls, parent: Optional[type['ContainerMixin']] = None) -> None:
        """Change the parent injection of this mixin.
        """
        cls.injection.change_parent(parent.injection if parent else None)

    @classmethod
    def update_dependencies(cls,
        imports: Iterable[type['ProviderMixin']] = (),
        partial_resolution: Optional[bool] = None,
        strict_resolution: Optional[bool] = None,
    ) -> None:
        """Register dependency imports and update resolution flags for this provider.

        Translates the list of ProviderMixin classes into their underlying
        Injectable objects and delegates to Injectable.update_dependencies.

        Args:
            imports (Iterable[type[ProviderMixin]]): Provider classes this provider
                depends on.
            partial_resolution (bool, optional): If True, imports outside the
                current provider set are not required to be resolved.
            strict_resolution (bool, optional): If False, resolution proceeds even
                when no implementation has been assigned.
        """
        cls.injectable.update_dependencies(
            imports={
                provider.injectable
                for provider in imports
            },
            partial_resolution=partial_resolution,
            strict_resolution=strict_resolution,
        )

    @classmethod
    def discard_dependencies(cls,
        imports: Iterable[type['ProviderMixin']] = (),
    ) -> None:
        """Remove dependencies from the provider.

        Args:
            imports (Iterable[type["ProviderMixin"]]): List of components to remove from imports.
        """
        cls.injectable.discard_dependencies(
            imports={
                provider.injectable
                for provider in imports
            },
        )

    @classmethod
    def reference(cls) -> str:
        """Return the reference name of the Injectable."""
        return cls.injection.reference

    @classmethod
    def provider(cls) -> providers.Provider[Any]:
        """Return the provider instance of the Injectable."""
        return cls.injection.provider

    @classmethod
    def provide(cls, *args: Any, **kwargs: Any) -> Any:
        """Provide an instance of the Injectable."""
        if not cls.injectable.is_resolved:
            raise DeclarationError(
                f"Injectable {cls.injection} accessed before being resolved. "
                f"Ensure it is declared as a dependency where it is being used."
            )
        return cls.injection.provider(*args, **kwargs)
