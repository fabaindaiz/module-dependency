from dependency.core.injection.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection

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
    containers: set[ContainerInjection]
    providers: set[ProviderInjection]
    @classmethod
    def register_container(cls, container: ContainerInjection) -> None:
        """Add a ContainerInjection node to the global registry.

        Called by ContainerMixin.init_injection when a @module or @plugin decorator
        is applied.

        Args:
            container (ContainerInjection): The container node to register.
        """
    @classmethod
    def register_provider(cls, provider: ProviderInjection) -> None:
        """Add a ProviderInjection node to the global registry.

        Called by ProviderMixin.init_injection when a @component or @product
        decorator is applied.

        Args:
            provider (ProviderInjection): The provider node to register.
        """
    @classmethod
    def validation(cls) -> None:
        """Warn about orphan containers and providers in the registry.

        An orphan is any injection node with no parent and is_root=False — meaning
        it was declared without being registered under any module or plugin. Orphan
        providers will be adopted by the FallbackPlugin during initialization, but
        this is a fallback mechanism and not the intended usage.

        This method only logs warnings; it does not raise exceptions.
        """
