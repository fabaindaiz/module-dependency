import logging
from pprint import pformat
from dependency.core.injection.injectable import Injectable
from dependency.core.resolution.container import Container
from dependency.core.resolution.utils import raise_providers_error
_logger = logging.getLogger("DependencyLoader")

class InjectionResolver:
    """Injection Resolver Class
    """
    def __init__(self, container: Container, injectables: list[Injectable]) -> None:
        self.container: Container = container
        self.injectables: list[Injectable] = injectables

    def resolve_dependencies(self) -> None:
        """Resolve all dependencies and initialize them."""
        _logger.info("Dependencies resolved and initialized")

    def resolve_injectables(self,
    ) -> list[list[Injectable]]:
        """Resolve all injectables in layers."""
        unresolved: list[Injectable] = self.injectables
        resolved_layers: list[list[Injectable]] = []

        while unresolved:
            new_layer = [
                implementation.wire_provider(container=self.container)
                for implementation in unresolved
                if implementation.import_resolved
            ]

            if len(new_layer) == 0:
                raise_providers_error(
                    injectables=self.injectables,
                    unresolved=unresolved
                )
            resolved_layers.append(new_layer)

            unresolved = [
                implementation
                for implementation in unresolved
                if not implementation.is_resolved
            ]
        named_laters = pformat(resolved_layers)
        _logger.info(f"Resolved layers:\n{named_laters}")
        return resolved_layers

    def start_implementations(self,
        resolved_layers: list[list[Injectable]],
    ) -> None:
        """Start all implementations by executing their bootstrap functions."""
        for layer in resolved_layers:
            for implementation in layer:
                implementation.do_bootstrap()
