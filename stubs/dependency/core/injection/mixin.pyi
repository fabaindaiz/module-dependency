from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection
from dependency.core.resolution.container import Container as Container
from dependency_injector import providers as providers
from typing import Any, Callable, Generator, Iterable

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
    @classmethod
    def resolve_providers(cls) -> Generator[Injectable, None, None]:
        """Resolve provider injections for the plugin.

        Returns:
            Generator[Injectable, None, None]: A generator of injectable providers.
        """

class ProviderMixin:
    """Providable Base Class

    Attributes:
        injection (ProviderInjection): Injection handler for the provider
    """
    injection: ProviderInjection
    @classmethod
    def init_injection(cls, parent: ContainerInjection | None) -> None: ...
    @classmethod
    def init_injectable(cls, wire_cls: Iterable[type], imports: Iterable[type['ProviderMixin']], products: Iterable[type['ProviderMixin']], provider: providers.Provider[Any], bootstrap: Callable[[], Any] | None) -> None: ...
    @classmethod
    def reference(cls) -> str:
        """Return the reference name of the Injectable."""
    @classmethod
    def provider(cls) -> providers.Provider[Any]:
        """Return the provider instance of the Injectable."""
    @classmethod
    def provide(cls, *args: Any, **kwargs: Any) -> Any:
        """Provide an instance of the Injectable."""
