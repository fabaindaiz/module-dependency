import logging
from pydantic import BaseModel
from typing import Optional
from dependency.core.injection.injectable import Injectable
from dependency.core.resolution.container import Container
from dependency.core.resolution.errors import raise_resolution_error
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

class ResolutionStrategy:
    """Defines the strategy for resolving dependencies.
    """
    def __init__(self,
        config: Optional[ResolutionConfig] = None
    ) -> None:
        self.config: ResolutionConfig = config or ResolutionConfig()

    def resolution(self,
        providers: list[Injectable],
        container: Container,
    ) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            providers (list[Injectable]): List of providers to resolve.
            container (Container): The container to wire the injectables with.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
        providers = self.expand(
            providers=providers
        )
        self.injection(
            providers=providers,
        )
        self.wiring(
            providers=providers,
            container=container,
        )
        self.initialize(
            providers=providers
        )
        return providers

    def expand(self,
        providers: list[Injectable],
    ) -> list[Injectable]:
        """Expand the list of providers by adding all their imports.

        Args:
            providers (list[Injectable]): List of providers to expand.

        Returns:
            list[Injectable]: List of expanded providers.
        """
        _logger.info("Expanding dependencies...")
        unexpanded: set[Injectable] = set(providers.copy())
        expanded: set[Injectable] = set()

        while unexpanded:
            provider: Injectable = unexpanded.pop()
            expanded.add(provider)

            if not provider.partial_resolution:
                unexpanded.update(filter(lambda i: i not in expanded, provider.imports))
        return list(expanded)

    def injection(self,
        providers: list[Injectable],
    ) -> None:
        """Resolve all injectables in layers.

        Args:
            providers (list[Injectable]): List of injectables to resolve.

        Returns:
            list[Injectable]: List of unresolved injectables.
        """
        _logger.info("Resolving dependencies...")
        unresolved: set[Injectable] = set(providers.copy())
        resolved: set[Injectable] = set()

        while unresolved:
            layer_resolved: set[Injectable] = set()
            layer_unresolved: set[Injectable] = set()

            for provider in unresolved:
                if provider.check_resolved(providers):
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
        providers: list[Injectable],
        container: Container,
    ) -> None:
        """Wire a list of providers with the given container.

        Args:
            providers (list[Injectable]): List of providers to wire.
            container (Container): The container to wire the providers with.
        """
        _logger.info("Wiring dependencies...")
        for provider in providers:
            container.wire(
                modules=provider.modules_cls,
                warn_unresolved=True,
            )
        if self.config.init_container:
            container.check_dependencies()
            container.init_resources()

    def initialize(self,
        providers: list[Injectable],
    ) -> None:
        """Start all implementations by executing their init functions.

        Args:
            providers (list[Injectable]): List of providers to start.
        """
        _logger.info("Initializing dependencies...")
        for provider in providers:
            if not provider.is_resolved:
                raise DeclarationError(
                    f"Injectable {provider} must be resolved before initialization. "
                    f"Ensure it is declared as a dependency where it is being used"
                )

            if provider.bootstrap is not None:
                try:
                    provider.bootstrap()
                except CancelInitialization as e:
                    _logger.warning(f"Injectable {provider} initialization skipped (cancelled by user): {e}")
                except Exception as e:
                    raise InitializationError(f"Injectable {provider} initialization failed") from e
