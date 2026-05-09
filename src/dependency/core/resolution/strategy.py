import logging
from pydantic import BaseModel
from typing import Iterable, Optional
from dependency.core.injection.injection import ProviderInjection
from dependency.core.resolution.container import Container
from dependency.core.resolution.errors import raise_resolution_error
from dependency.core.resolution.expansion import ProviderExpansion
from dependency.core.exceptions import (
    DeclarationError,
    InitializationError,
    CancelInitialization,
)
_logger = logging.getLogger("dependency.loader")

class ResolutionConfig(BaseModel):
    """Configuration for the Resolution Strategy.
    """
    init_container: bool = True
    legacy_resolution: bool = False

class ResolutionStrategy:
    """Defines the strategy for resolving dependencies.
    """
    def __init__(self,
        config: Optional[ResolutionConfig] = None
    ) -> None:
        self.config: ResolutionConfig = config or ResolutionConfig()

    def expand(self,
        providers: set[ProviderInjection],
    ) -> set[ProviderInjection]:
        """Expand a seed set of providers by following imports transitively.

        Raises ResolutionError if any required dependency could not be resolved.
        """
        result = ProviderExpansion(modules=[], extra=providers).expand()
        result.raise_if_failed()
        return result.resolved

    def resolution(self,
        providers: set[ProviderInjection],
        container: Container,
    ) -> set[ProviderInjection]:
        providers = self.expand(providers)
        self.injection(providers=providers)
        self.wiring(providers=providers, container=container)
        self.initialize(providers=providers)
        return providers

    def injection(self,
        providers: set[ProviderInjection],
    ) -> None:
        """Resolve all providers in dependency order (layer by layer)."""
        _logger.info("Resolving dependencies...")
        unresolved: set[ProviderInjection] = providers.copy()
        resolved: set[ProviderInjection] = set()

        while unresolved:
            layer_resolved: set[ProviderInjection] = set()
            layer_unresolved: set[ProviderInjection] = set()

            for provider in unresolved:
                if provider.resolve_if_posible(providers):
                    layer_resolved.add(provider)
                else:
                    layer_unresolved.add(provider)

            if not layer_resolved:
                raise_resolution_error(
                    providers=providers,
                    unresolved=list(unresolved),
                )

            resolved.update(layer_resolved)
            unresolved = layer_unresolved

    def wiring(self,
        providers: Iterable[ProviderInjection],
        container: Container,
    ) -> None:
        """Wire providers against the application container."""
        _logger.info("Wiring dependencies...")
        for provider in providers:
            container.wire(
                modules=provider.injectable.modules_cls,
                warn_unresolved=True,
            )
        if self.config.init_container:
            container.check_dependencies()
            container.init_resources()

    def initialize(self,
        providers: Iterable[ProviderInjection],
    ) -> None:
        """Execute bootstrap callables for eagerly-instantiated providers."""
        _logger.info("Initializing dependencies...")
        for provider in providers:
            if not provider.is_resolved:
                raise DeclarationError(
                    f"Injectable {provider} must be resolved before initialization. "
                    f"Ensure it is declared as a dependency where it is being used"
                )

            if provider.injectable.bootstrap is not None:
                try:
                    provider.injectable.bootstrap()
                except CancelInitialization as e:
                    _logger.warning(f"Injectable {provider} initialization skipped (cancelled by user): {e}")
                except Exception as e:
                    raise InitializationError(f"Injectable {provider} initialization failed") from e
