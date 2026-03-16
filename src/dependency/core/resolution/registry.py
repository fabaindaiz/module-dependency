import logging
from dependency.core.injection.injection import ContainerInjection, ProviderInjection
_logger = logging.getLogger("dependency.loader")

class Registry:
    containers: set[ContainerInjection] = set()
    providers: set[ProviderInjection] = set()

    @classmethod
    def register_container(cls, container: ContainerInjection) -> None:
        cls.containers.add(container)

    @classmethod
    def register_provider(cls, provider: ProviderInjection) -> None:
        cls.providers.add(provider)

    @classmethod
    def validation(cls) -> None:
        for container in cls.containers:
            if container.parent is None and not container.is_root:
                _logger.warning(f"Container {container} has no parent module (consider registering)")
        for provider in cls.providers:
            if provider.parent is None and not provider.is_root:
                _logger.warning(f"Provider {provider} has no parent module (consider registering)")
