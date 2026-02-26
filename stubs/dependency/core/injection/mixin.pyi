from dependency.core.exceptions import DeclarationError as DeclarationError
from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection
from dependency.core.injection.wiring import WiringMixin as WiringMixin
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.registry import Registry as Registry
from dependency_injector import providers as providers
from typing import Any, Callable, Generator, Iterable

class ContainerMixin:
    """Container Mixin Class

    Attributes:
        injection (ContainerInjection): Injection handler for the container
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
    def resolve_injectables(cls) -> Generator[Injectable, None, None]:
        """Resolve provider injections for the plugin.

        Returns:
            Generator[Injectable, None, None]: A generator of injectables.
        """

class ProviderMixin(WiringMixin):
    """Providable Base Class

    Attributes:
        injection (ProviderInjection): Injection handler for the provider
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
    def update_dependencies(cls, imports: Iterable[type['ProviderMixin']] = (), partial_resolution: bool | None = None) -> None:
        '''Initialize the dependencies for the provider.

        Args:
            imports (Iterable[type["ResolubleClass"]]): List of providers to be imported by the provider.
            partial_resolution (bool, optional): Whether to allow partial resolution of dependencies. Defaults to False.
        '''
    @classmethod
    def discard_dependencies(cls, imports: Iterable[type['ProviderMixin']] = ()) -> None:
        '''Remove dependencies from the provider.

        Args:
            imports (Iterable[type["ProviderMixin"]]): List of components to remove from imports.
            products (Iterable[type["ProviderMixin"]]): List of components to remove from products.
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
