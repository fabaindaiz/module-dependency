import logging
from pydantic import BaseModel
from dependency.core.injection.injectable import Injectable
from dependency.core.injection.resoluble import ResolubleProvider
from dependency.core.resolution.container import Container
from dependency.core.resolution.errors import raise_resolution_error
_logger = logging.getLogger("dependency.loader")

class ResolutionConfig(BaseModel):
    """Configuration for the Resolution Strategy.
    """
    init_container: bool = True
    resolve_products: bool = True

class ResolutionStrategy:
    """Defines the strategy for resolving dependencies.
    """
    config: ResolutionConfig = ResolutionConfig()

    @classmethod
    def resolution(cls,
        container: Container,
        providers: list[ResolubleProvider],
    ) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            container (Container): The container to wire the injectables with.
            providers (list[ProviderInjection]): List of provider injections to resolve.
            config (ResolutionConfig): Configuration for the resolution strategy.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
        injectables: list[Injectable] = cls.injection(
            providers=providers,
        )
        cls.wiring(
            container=container,
            injectables=injectables,
        )
        cls.initialize(
            injectables=injectables
        )
        return injectables

    @classmethod
    def injection(cls,
        providers: list[ResolubleProvider],
    ) -> list[Injectable]:
        """Resolve all injectables in layers.

        Args:
            providers (list[ResolubleClass]): List of resoluble classes to resolve.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
        _logger.info("Resolving dependencies...")
        unresolved: list[ResolubleProvider] = providers.copy()
        resolved: list[ResolubleProvider] = []
        layer_count: int = 0

        while unresolved:
            new_layer = [
                provider.inject()
                for provider in unresolved
                if provider.import_resolved
            ]

            if len(new_layer) == 0:
                raise_resolution_error(
                    providers=providers,
                    unresolved=unresolved
                )
            resolved.extend(new_layer)
            _logger.debug(f"Layer {layer_count}: {new_layer}")
            layer_count += 1

            if cls.config.resolve_products:
                for provider in new_layer:
                    unresolved.extend(provider.products)

            unresolved = [
                provider
                for provider in unresolved
                if not provider.is_resolved
            ]
        return [
            provider.injectable
            for provider in resolved
        ]

    @classmethod
    def wiring(cls,
        container: Container,
        injectables: list[Injectable],
    ) -> None:
        """Wire a list of injectables with the given container.

        Args:
            container (Container): The container to wire the injectables with.
            injectables (list[Injectable]): List of injectables to wire.
        """
        _logger.info("Wiring dependencies...")
        for injectable in injectables:
            injectable.wire(container=container)
        if cls.config.init_container:
            container.check_dependencies()
            container.init_resources()

    @classmethod
    def initialize(cls,
        injectables: list[Injectable],
    ) -> None:
        """Start all implementations by executing their init functions.

        Args:
            injectables (list[Injectable]): List of injectables to start.
        """
        _logger.info("Initializing dependencies...")
        for injectable in injectables:
            injectable.init()
