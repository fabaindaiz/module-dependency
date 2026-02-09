from typing import Any, Callable, Generator, Iterable, Optional
from dependency_injector import providers
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.injection import ContainerInjection, ProviderInjection
from dependency.core.resolution.container import Container

class ContainerMixin:
    """Container Mixin Class

    Attributes:
        injection (ContainerInjection): Injection handler for the container
    """
    injection: ContainerInjection

    @classmethod
    def inject_container(cls, container: Container) -> None:
        """Inject the module into the application container.

        Args:
            container (Container): The application container.
        """
        setattr(container, cls.injection.name, cls.injection.inject_cls())

    @classmethod
    def resolve_providers(cls) -> Generator[Injectable, None, None]:
        """Resolve provider injections for the plugin.

        Returns:
            Generator[Injectable, None, None]: A generator of injectable providers.
        """
        return (provider for provider in cls.injection.resolve_providers())

class ProviderMixin:
    """Providable Base Class

    Attributes:
        injection (ProviderInjection): Injection handler for the provider
    """
    injection: ProviderInjection

    @classmethod
    def init_injection(cls,
        parent: Optional[ContainerInjection]
    ) -> None:
        cls.injection = ProviderInjection(
            name=cls.__name__,
            interface_cls=cls,
            parent=parent,
        )

    @classmethod
    def init_injectable(cls,
        wire_cls: Iterable[type],
        imports: Iterable[type["ProviderMixin"]],
        products: Iterable[type["ProviderMixin"]],
        provider: providers.Provider[Any],
        bootstrap: Optional[Callable[[], Any]]
    ) -> None:

        cls.injection.set_instance(
            injectable=Injectable(
                component_cls=cls,
                provided_cls=[cls, *wire_cls],
                provider=provider,
                imports=(
                    provider.injection.injectable
                    for provider in imports
                ),
                products=(
                    provider.injection.injectable
                    for provider in products
                ),
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
