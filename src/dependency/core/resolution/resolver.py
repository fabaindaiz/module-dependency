import logging
from pydantic import BaseModel
from typing import Iterable
from dependency.core.injection.injectable import Injectable
from dependency.core.resolution.container import Container
from dependency.core.resolution.errors import raise_resolution_error
_logger = logging.getLogger("dependency.loader")

class InjectionConfig(BaseModel):
    """Configuration for the Injection Resolver.
    """
    resolve_products: bool = True

# TODO: añadir API meta con acceso al framework
class InjectionResolver:
    """Injection Resolver Class
    """
    def __init__(self,
        container: Container,
        injectables: Iterable[Injectable],
    ) -> None:
        self.container: Container = container
        self._injectables: list[Injectable] = list(injectables)

    def resolve_dependencies(self,
        config: InjectionConfig = InjectionConfig()
    ) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            config (InjectionConfig): Configuration for the injection resolver.

        Returns:
            list[Injectable]: List of resolved injectables."""
        return self.resolution(
            container=self.container,
            injectables=self._injectables,
            config=config,
        )

    @classmethod
    def resolution(cls,
        container: Container,
        injectables: list[Injectable],
        config: InjectionConfig = InjectionConfig(),
    ) -> list[Injectable]:
        """Resolve all dependencies and initialize them.

        Args:
            container (Container): The container to wire the injectables with.
            injectables (list[Injectable]): List of injectables to resolve.
            config (InjectionConfig): Configuration for the injection resolver.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
        injectables = cls.injection(
            injectables=injectables,
            config=config,
        )
        cls.wiring(
            container=container,
            injectables=injectables,
        )
        cls.bootstrap(
            injectables=injectables
        )
        return injectables

    @staticmethod
    def injection(
        injectables: list[Injectable],
        config: InjectionConfig = InjectionConfig(),
    ) -> list[Injectable]:
        """Resolve all injectables in layers.

        Args:
            container (Container): The container to wire the injectables with.
            injectables (list[Injectable]): List of injectables to resolve.

        Returns:
            list[Injectable]: List of resolved injectables.
        """
        _logger.info("Resolving injectables...")
        unresolved: list[Injectable] = injectables.copy()
        resolved: list[Injectable] = []

        while unresolved:
            new_layer = [
                injectable.do_resolve()
                for injectable in unresolved
                if injectable.import_resolved
            ]

            if len(new_layer) == 0:
                raise_resolution_error(
                    injectables=injectables,
                    unresolved=unresolved
                )
            resolved.extend(new_layer)
            _logger.debug(f"Layer: {new_layer}")

            if config.resolve_products:
                for injectable in new_layer:
                    unresolved.extend(injectable.products)

            unresolved = [
                injectable
                for injectable in unresolved
                if not injectable.is_resolved
            ]
        return resolved

    @staticmethod
    def wiring(
        container: Container,
        injectables: list[Injectable],
    ) -> None:
        """Wire a list of injectables with the given container.

        Args:
            container (Container): The container to wire the injectables with.
            injectables (list[Injectable]): List of injectables to wire.
        """
        _logger.info("Wiring injectables...")
        for injectable in injectables:
            injectable.do_wiring(container=container)
        container.initialize()

    @staticmethod
    def bootstrap(
        injectables: list[Injectable],
    ) -> None:
        """Start all implementations by executing their bootstrap functions.

        Args:
            injectables (list[Injectable]): List of injectables to start.
        """
        _logger.info("Starting injectables...")
        for injectable in injectables:
            injectable.do_bootstrap()
