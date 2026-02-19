import logging
from pydantic import BaseModel
from dependency.core.injection.injectable import Injectable
from dependency.core.resolution.container import Container
from dependency.core.resolution.errors import raise_resolution_error
_logger = logging.getLogger("dependency.loader")

class ResolutionConfig(BaseModel):
    """Configuration for the Resolution Strategy.
    """
    init_container: bool = True

class ResolutionStrategy:
    """Defines the strategy for resolving dependencies.
    """
    config: ResolutionConfig = ResolutionConfig()

    @classmethod
    def resolution(cls,
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
        providers = cls.expand(
            providers=providers
        )
        cls.injection(
            providers=providers,
        )
        cls.wiring(
            providers=providers,
            container=container,
        )
        cls.initialize(
            providers=providers
        )
        return providers

    @classmethod
    def expand(cls,
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

    @classmethod
    def injection(cls,
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

    @classmethod
    def validation(cls,
        providers: list[Injectable],
        unresolved: list[Injectable],
    ) -> None:
        """Validate that all unresolved injectables are in the list of providers.

        Args:
            providers (list[Injectable]): List of providers to validate.
            unresolved (list[Injectable]): List of unresolved injectables.
        """
        if unresolved:
            _logger.warning(f"Unresolved injectables: {unresolved}")


    @classmethod
    def wiring(cls,
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
            provider.wire(container=container)
        if cls.config.init_container:
            container.check_dependencies()
            container.init_resources()

    @classmethod
    def initialize(cls,
        providers: list[Injectable],
    ) -> None:
        """Start all implementations by executing their init functions.

        Args:
            providers (list[Injectable]): List of providers to start.
        """
        _logger.info("Initializing dependencies...")
        for provider in providers:
            provider.init()
