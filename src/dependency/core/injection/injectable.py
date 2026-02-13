import logging
from typing import Any, Callable, Optional
from dependency_injector import containers, providers
from dependency.core.exceptions import (
    DeclarationError,
    InitializationError,
    CancelInitialization,
)
_logger = logging.getLogger("dependency.loader")

class Injectable:
    """Injectable Class represents a implementation of some kind that can be injected as a dependency.

    Attributes:
        interface_cls (T): The interface class that this injectable implements.

        imports (Iterable[Injectable]): List of injectables that this injectable depends on.
        products (Iterable[Injectable]): List of injectables that depend on this injectable.
    """
    def __init__(self,
        interface_cls: type,
        modules_cls: set[type],
        provider: providers.Provider[Any],
        bootstrap: Optional[Callable[[], Any]] = None
    ) -> None:
        self.interface_cls: type = interface_cls
        self.modules_cls: set[type] = {interface_cls, *modules_cls}
        self.provider_cls: providers.Provider[Any] = provider
        self._bootstrap: Optional[Callable[[], Any]] = bootstrap
        self.is_resolved: bool = False

    @property
    def provider(self) -> providers.Provider[Any]:
        """Return an instance from the provider."""
        if not self.is_resolved:
            raise DeclarationError(
                f"Injectable {self.interface_cls.__name__} accessed before being resolved. "
                f"Ensure it is declared as a dependency (imports or products) where it is being used"
            )
        return self.provider_cls

    def inject(self) -> None:
        """Mark the injectable as resolved."""
        self.is_resolved = True

    def wire(self, container: containers.DynamicContainer) -> None:
        """Wire the provider with the given container.

        Args:
            container (containers.DynamicContainer): Container to wire the provider with.
        """
        container.wire(
            modules=self.modules_cls,
            warn_unresolved=True,
        )

    def init(self) -> None:
        """Execute the bootstrap function if it exists."""
        if not self.is_resolved:
            raise DeclarationError(
                f"Injectable {self.interface_cls.__name__} must be resolved before initialization. "
                f"Ensure it is declared as a dependency (imports or products) where it is being used"
            )

        if self._bootstrap is not None:
            try:
                self._bootstrap()
            except CancelInitialization as e:
                _logger.warning(f"Injectable {self.interface_cls.__name__} initialization skipped (cancelled by user): {e}")
            except Exception as e:
                raise InitializationError(f"Injectable {self.interface_cls.__name__} initialization failed") from e

    def __repr__(self) -> str:
        return f"{self.interface_cls.__name__}"
