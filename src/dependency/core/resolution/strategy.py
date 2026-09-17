import logging
from dependency_injector import providers as providers_module
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
    """Configuration for the Resolution Strategy."""

    init_container: bool = True
    legacy_resolution: bool = False


class ResolutionStrategy:
    """Defines the strategy for resolving dependencies."""

    def __init__(self, config: Optional[ResolutionConfig] = None) -> None:
        self.config: ResolutionConfig = config or ResolutionConfig()

    def expand(
        self,
        providers: set[ProviderInjection],
    ) -> set[ProviderInjection]:
        """Expand a seed set of providers by following imports transitively.

        Raises ResolutionError if any required dependency could not be resolved.
        """
        result = ProviderExpansion(modules=[], extra=providers).expand()
        result.raise_if_failed()
        return result.resolved

    def resolution(
        self,
        providers: set[ProviderInjection],
        container: Container,
    ) -> list[ProviderInjection]:
        providers = self.expand(providers)
        order = self.injection(providers=providers)
        self.wiring(providers=providers, container=container)
        self.initialize(providers=order)
        return order

    def injection(
        self,
        providers: set[ProviderInjection],
    ) -> list[ProviderInjection]:
        """Resolve all providers in dependency order (layer by layer).

        Returns the order it resolved them in, which this method has always computed and
        used to throw away: every provider appears after all of its required imports, and
        providers that became resolvable together are ordered by name so two runs of the
        same graph produce the same sequence. `initialize` consumes it, which is what makes
        bootstrap order a contract instead of `set` iteration (D-053).

        Returns:
            list[ProviderInjection]: Dependency order, then name order within a layer.
        """
        _logger.info("Resolving dependencies...")
        unresolved: set[ProviderInjection] = providers.copy()
        order: list[ProviderInjection] = []

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

            order.extend(sorted(layer_resolved, key=lambda provider: provider.name))
            unresolved = layer_unresolved

        return order

    def shutdown(
        self,
        providers: Iterable[ProviderInjection],
    ) -> None:
        """Shut down every `Resource`-backed provider, in reverse of the order given.

        The mirror of `initialize`: pass the list `resolution` returned and a provider is
        torn down before the providers it imports, which is the only order in which a
        dependency is still alive while its dependents stop using it.

        This exists because the root `Container` cannot reach plugin providers — its own
        `.providers` is `['__self__']`, since plugin providers live in nested
        sub-containers attached with `setattr` — so `container.shutdown_resources()`
        silently reaches none of them (D-034). Every application had to walk the tree by
        hand; now the framework does (D-055).
        """
        _logger.info("Shutting down resources...")
        for provider in reversed(list(providers)):
            if not isinstance(provider.provider, providers_module.Resource):
                continue
            try:
                provider.provider.shutdown()
            except Exception as error:  # noqa: BLE001 - one bad teardown must not strand the rest
                _logger.warning(f"Injectable {provider} shutdown failed: {error}")

    def wiring(
        self,
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

    def initialize(
        self,
        providers: Iterable[ProviderInjection],
    ) -> None:
        """Execute bootstrap callables in the order given.

        Pass the list `injection` returned: a provider's required imports then bootstrap
        before it, which is what most people assume and what nothing guaranteed before
        (D-053). Passing a `set` restores the old unspecified order.
        """
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
                    _logger.warning(
                        f"Injectable {provider} initialization skipped (cancelled by user): {e}"
                    )
                except Exception as e:
                    raise InitializationError(
                        f"Injectable {provider} initialization failed"
                    ) from e
