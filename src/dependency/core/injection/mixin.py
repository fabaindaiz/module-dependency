import logging
from typing import Any, Callable, Generator, Iterable, Optional, cast
from dependency_injector import providers
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.injection import ContainerInjection
from dependency.core.injection.resoluble import ResolubleProvider
from dependency.core.resolution.container import Container
_logger = logging.getLogger("dependency.loader")

class ContainerMixin:
    """Container Mixin Class

    Attributes:
        injection (ContainerInjection): Injection handler for the container
    """
    injection: ContainerInjection
    is_root: bool = False

    @classmethod
    def init_injection(cls,
        parent: Optional[ContainerInjection],
    ) -> None:
        """Initialize the injection for the container.

        Args:
            parent (Optional[ContainerInjection]): Parent container injection instance.
        """
        if parent is None and not cls.is_root:
            _logger.warning(f"Container {cls.__name__} has no parent module (consider registering)")

        cls.injection = ContainerInjection(
            name=cls.__name__,
            parent=parent,
        )

    @classmethod
    def inject_container(cls, container: Container) -> None:
        """Inject the module into the application container.

        Args:
            container (Container): The application container.
        """
        setattr(container, cls.injection.name, cls.injection.inject_cls())

    @classmethod
    def resolve_providers(cls) -> Generator['ResolubleProvider', None, None]:
        """Resolve provider injections for the plugin.

        Returns:
            Generator[ResolubleClass, None, None]: A generator of resoluble classes.
        """
        return (
            cast(ResolubleProvider, provider)
            for provider in cls.injection.resolve_providers()
        )

class ProviderMixin:
    """Providable Base Class

    Attributes:
        injection (ProviderInjection): Injection handler for the provider
    """
    injection: ResolubleProvider

    @classmethod
    def init_injection(cls,
        parent: Optional[ContainerInjection],
    ) -> None:
        """Initialize the injection for the provider.

        Args:
            parent (Optional[ContainerInjection]): Parent container injection instance.
        """
        if parent is None:
            _logger.warning(f"Provider {cls.__name__} has no parent module (consider registering)")

        cls.injection = ResolubleProvider(
            name=cls.__name__,
            interface_cls=cls,
            parent=parent,
        )

    @classmethod
    def init_dependencies(cls,
        imports: Iterable[type['ProviderMixin']],
        products: Iterable[type['ProviderMixin']],
        partial_resolution: bool = False,
    ) -> None:
        """Initialize the dependencies for the provider.

        Args:
            imports (Iterable[type["ResolubleClass"]]): List of components to be imported by the provider.
            products (Iterable[type["ResolubleClass"]]): List of products to be declared by the provider.
        """
        cls.injection.add_dependencies(
            imports={
                injection.injection.as_import(cls.injection)
                for injection in imports
            },
            products={
                injection.injection.as_product(cls.injection)
                for injection in products
            },
            partial_resolution=partial_resolution,
        )

    @classmethod
    def init_injectable(cls,
        modules_cls: Iterable[type],
        provider: providers.Provider[Any],
        bootstrap: Optional[Callable[[], Any]]
    ) -> None:
        """Initialize the injectable for the provider.

        Args:
            modules_cls (Iterable[type]): List of modules that need to be wired for the provider.
            provider (providers.Provider[Any]): Provider instance to be used for the injectable.
            imports (Iterable[type["ProviderMixin"]]): List of components to be imported by the provider.
            products (Iterable[type["ProviderMixin"]]): List of products to be declared by the provider.
            bootstrap (Optional[Callable[[], Any]]): Whether the provider should be bootstrapped.

        Raises:
            TypeError: _description_
        """
        interface_cls: type = cls.injection.interface_cls
        if not issubclass(cls, interface_cls):
            raise TypeError(f"Class {cls.__name__} must be a subclass of {interface_cls.__name__} to be used as an instance of component {cls.__name__}")

        cls.injection.set_injectable(
            injectable=Injectable(
                interface_cls=cls,
                modules_cls={cls, *modules_cls},
                provider=provider,
                bootstrap=bootstrap,
            )
        )

    @classmethod
    def reference(cls) -> str:
        """Return the reference name of the Injectable."""
        return cls.injection.reference

    @classmethod
    def provider(cls) -> providers.Provider[Any]:
        """Return the provider instance of the Injectable."""
        return cls.injection.injectable.provider

    @classmethod
    def provide(cls, *args: Any, **kwargs: Any) -> Any:
        """Provide an instance of the Injectable."""
        return cls.injection.injectable.provider(*args, **kwargs)
