import logging
from dependency.core.injection.injection import ContainerInjection, ProviderInjection
_logger = logging.getLogger("dependency.loader")

class Registry:
    """Global store for all injection nodes created at decoration time.

    The Registry is populated when @module, @component, @instance, and @product
    decorators are applied — before any resolution happens. It tracks every
    ContainerInjection and ProviderInjection ever created in the process, allowing
    cross-cutting validation and the FallbackPlugin to discover orphan providers.

    This is class-level (shared) state. In test environments, the sets should be
    cleared between test runs to avoid state leaking across tests.

    Attributes:
        containers (set[ContainerInjection]): All registered container injection nodes.
        providers (set[ProviderInjection]): All registered provider injection nodes.
    """
    containers: set[ContainerInjection] = set()
    providers: set[ProviderInjection] = set()

    @classmethod
    def register_container(cls, container: ContainerInjection) -> None:
        """Add a ContainerInjection node to the global registry.

        Called by ContainerMixin.init_injection when a @module or @plugin decorator
        is applied.

        Args:
            container (ContainerInjection): The container node to register.
        """
        cls.containers.add(container)

    @classmethod
    def register_provider(cls, provider: ProviderInjection) -> None:
        """Add a ProviderInjection node to the global registry.

        Called by ProviderMixin.init_injection when a @component or @product
        decorator is applied.

        Args:
            provider (ProviderInjection): The provider node to register.
        """
        cls.providers.add(provider)

    @classmethod
    def validation(cls) -> None:
        """Warn about orphan containers and providers in the registry.

        An orphan is any injection node with no parent and is_root=False — meaning
        it was declared without being registered under any module or plugin. Orphan
        providers will be adopted by the FallbackPlugin during initialization, but
        this is a fallback mechanism and not the intended usage.

        This method only logs warnings; it does not raise exceptions.
        """
        for container in cls.containers:
            if container.parent is None and not container.is_root:
                _logger.warning(f"Container {container} has no parent module (consider registering)")
        for provider in cls.providers:
            if provider.parent is None and not provider.is_root:
                _logger.warning(f"Provider {provider} has no parent module (consider registering)")
