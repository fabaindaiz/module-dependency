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
        providers = cls.injection(
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
    def injection(cls,
        providers: list[Injectable],
    ) -> list[Injectable]:
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
            layer_resolved: set[Injectable] = set(
                filter(lambda p: p.check_resolved, unresolved)
            )
            layer_unresolved: set[Injectable] = set(
                filter(lambda p: not p.is_resolved, unresolved)
            )

            if not layer_resolved:
                raise_resolution_error(
                    providers=providers,
                    unresolved=list(unresolved),
                )

            resolved.update(layer_resolved)
            unresolved = layer_unresolved

        return list(resolved)

    @classmethod
    def injection(cls,
        providers: list[Injectable],
    ) -> list[Injectable]:
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
            layer_resolved: set[Injectable] = set(
                filter(lambda p: p.check_resolved, unresolved)
            )
            layer_unresolved: set[Injectable] = set(
                filter(lambda p: not p.is_resolved, unresolved)
            )

            new_unresolved: set[Injectable] = set()
            for provider in layer_unresolved:
                if not provider.partial_resolution:
                    new_unresolved.update(filter(lambda i: not i.is_resolved, provider.imports))

            if not layer_resolved:
                raise_resolution_error(
                    providers=providers,
                    unresolved=list(unresolved),
                )

            resolved.update(layer_resolved)
            unresolved = layer_unresolved

        return list(resolved)

    @classmethod
    def injection2(cls,
        providers: list[Injectable],
    ) -> list[Injectable]:

            new_unresolved: set[Injectable] = set()
            for provider in layer_unresolved:
                if not provider.partial_resolution:
                    new_unresolved.update(filter(lambda i: not i.is_resolved and i not in unresolved, provider.imports))







            if not layer_resolved:


                if new_unresolved:
                    unresolved.update(new_unresolved)

                    raise_resolution_error(
                        providers=providers,
                        unresolved=list(unresolved),
                    )

                unresolved.update(new_unresolved)





            if not new_layer:
                imports: set[Injectable] = set()
                for provider in unresolved:
                    imports.update(filter(lambda i: not i.is_resolved, provider.imports))

                if all(provider.check_resolution for provider in imports):
                    unresolved = set(filter(lambda p: not p.is_resolved, unresolved))
                    continue

                raise_resolution_error(
                    providers=providers,
                    unresolved=list(unresolved),
                )

            resolved.update(new_layer)

            for provider in unresolved:
                unresolved.update(filter(lambda d: not d.is_resolved, provider.imports))

        return list(resolved)

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
