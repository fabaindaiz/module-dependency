from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.injection import ContainerInjection as ContainerInjection
from dependency.core.injection.resoluble import ResolubleProvider as ResolubleProvider
from dependency.core.resolution.container import Container as Container
from dependency_injector import providers as providers
from typing import Any, Callable, Generator, Iterable

class ContainerMixin:
    """Container Mixin Class

    Attributes:
        injection (ContainerInjection): Injection handler for the container
    """
    injection: ContainerInjection
    is_root: bool
    @classmethod
    def init_injection(cls, parent: ContainerInjection | None) -> None:
        """Initialize the injection for the container.

        Args:
            parent (Optional[ContainerInjection]): Parent container injection instance.
        """
    @classmethod
    def inject_container(cls, container: Container) -> None:
        """Inject the module into the application container.

        Args:
            container (Container): The application container.
        """
    @classmethod
    def resolve_providers(cls) -> Generator['ResolubleProvider', None, None]:
        """Resolve provider injections for the plugin.

        Returns:
            Generator[ResolubleClass, None, None]: A generator of resoluble classes.
        """

class ProviderMixin:
    """Providable Base Class

    Attributes:
        injection (ProviderInjection): Injection handler for the provider
    """
    injection: ResolubleProvider
    @classmethod
    def init_injection(cls, parent: ContainerInjection | None) -> None:
        """Initialize the injection for the provider.

        Args:
            parent (Optional[ContainerInjection]): Parent container injection instance.
        """
    @classmethod
    def init_dependencies(cls, imports: Iterable[type['ProviderMixin']], products: Iterable[type['ProviderMixin']], partial_resolution: bool = False) -> None:
        '''Initialize the dependencies for the provider.

        Args:
            imports (Iterable[type["ResolubleClass"]]): List of components to be imported by the provider.
            products (Iterable[type["ResolubleClass"]]): List of products to be declared by the provider.
        '''
    @classmethod
    def init_injectable(cls, modules_cls: Iterable[type], provider: providers.Provider[Any], bootstrap: Callable[[], Any] | None) -> None:
        '''Initialize the injectable for the provider.

        Args:
            modules_cls (Iterable[type]): List of modules that need to be wired for the provider.
            provider (providers.Provider[Any]): Provider instance to be used for the injectable.
            imports (Iterable[type["ProviderMixin"]]): List of components to be imported by the provider.
            products (Iterable[type["ProviderMixin"]]): List of products to be declared by the provider.
            bootstrap (Optional[Callable[[], Any]]): Whether the provider should be bootstrapped.

        Raises:
            TypeError: _description_
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
