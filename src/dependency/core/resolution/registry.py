import logging
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.injection import ProviderInjection
_logger = logging.getLogger("dependency.loader")

class Registry:
    providers: set[ProviderInjection] = set()

    @classmethod
    def register(cls, provider: ProviderInjection) -> None:
        cls.providers.add(provider)

    @classmethod
    def validation(cls) -> None:
        for provider in cls.providers:
            if provider.parent is None and not provider.is_root:
                _logger.warning(f"Provider {provider} has no parent module (consider registering)")

            injectable: Injectable = provider.injectable
