from dependency.core.exceptions import DeclarationError as DeclarationError
from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection
from dependency.core.injection.wiring import WiringMixin as WiringMixin
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.registry import Registry as Registry
from dependency_injector import containers as containers, providers as providers
from typing import Any, Callable, Generator, Iterable

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
    def init_injection(cls, parent: ContainerInjection | None) -> None:
        """Initialize the injection for the container.

        Args:
            parent (Optional[ContainerInjection]): Parent container injection instance.
        """
    @classmethod
    def change_parent(cls, parent: ContainerMixin | None = None) -> None:
        """Change the parent injection of this mixin.

        Args:
            parent (ContainerMixin): The new parent container.
        """
    @classmethod
    def inject_container(cls, container: Container) -> None:
        """Inject the module into the application container.

        Args:
            container (Container): The application container.
        """
    @classmethod
    def resolve_providers(cls, container: containers.Container | None = None) -> None:
        """Resolve all child providers into this container's DynamicContainer.

        Delegates to ContainerInjection.resolve_providers, which recursively
        attaches each child ProviderInjection to the appropriate sub-container.

        Args:
            container (containers.Container, optional): If provided, also attaches
                this container as an attribute of the given parent container.
        """
    @classmethod
    def resolve_injectables(cls) -> Generator[Injectable, None, None]:
        """Yield all Injectable objects registered under this container.

        Walks the ContainerInjection tree and yields every Injectable found in
        child ProviderInjection nodes. Used during Phase 2 of resolution to
        collect the full set of providers to resolve.

        Returns:
            Generator[Injectable, None, None]: A generator of injectables.
        """

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
    def init_injection(cls, parent: ContainerInjection | None) -> None:
        """Initialize the injection for the provider.

        Args:
            parent (Optional[ContainerInjection]): Parent container injection instance.
        """
    @classmethod
    def init_implementation(cls, modules_cls: Iterable[type], provider: providers.Provider[Any], bootstrap: Callable[[], Any] | None) -> None:
        """Initialize the injectable for the provider.

        Args:
            modules_cls (Iterable[type]): List of modules that need to be wired for the provider.
            provider (providers.Provider[Any]): Provider instance to be used for the injectable.
            bootstrap (Optional[Callable[[], Any]]): Whether the provider should be bootstrapped.

        Raises:
            TypeError: If the class is not a subclass of the interface class.
        """
    @classmethod
    def change_parent(cls, parent: type['ContainerMixin'] | None = None) -> None:
        """Change the parent injection of this mixin.
        """
    @classmethod
    def update_dependencies(cls, imports: Iterable[type['ProviderMixin']] = (), partial_resolution: bool | None = None, strict_resolution: bool | None = None) -> None:
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
    @classmethod
    def discard_dependencies(cls, imports: Iterable[type['ProviderMixin']] = ()) -> None:
        '''Remove dependencies from the provider.

        Args:
            imports (Iterable[type["ProviderMixin"]]): List of components to remove from imports.
        '''
    @classmethod
    def reference(cls) -> str:
        """Return the reference name of the Injectable."""
    @classmethod
    def provider(cls) -> providers.Provider[Any]:
        """Return the provider instance of the Injectable."""
    @classmethod
    def provide(cls, *args: Any, **kwargs: Any) -> Any:
        """Provide an instance of the Injectable."""
