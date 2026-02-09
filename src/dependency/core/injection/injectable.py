import logging
from typing import Any, Callable, Iterable, Optional
from dependency_injector import containers, providers
from dependency.core.utils.lazy import LazyList
from dependency.core.exceptions import (
    DeclarationError,
    InitializationError,
    CancelInitialization,
)
_logger = logging.getLogger("dependency.loader")

class Injectable:
    """Injectable Class representing a injectable dependency.
    """
    def __init__(self,
        component_cls: type,
        modules_cls: set[type],
        provider: providers.Provider[Any],
        imports: Iterable['Injectable'] = (),
        products: Iterable['Injectable'] = (),
        bootstrap: Optional[Callable[[], Any]] = None
    ) -> None:
        self.needs_full_resolution: bool = False

        self.component_cls: type = component_cls
        self.modules_cls: set[type] = {component_cls, *modules_cls}
        self.provider_cls: providers.Provider[Any] = provider
        self._imports: LazyList['Injectable'] = LazyList(imports)
        self._products: LazyList['Injectable'] = LazyList(products)
        self._bootstrap: Optional[Callable[[], Any]] = bootstrap
        self.is_resolved: bool = False

    @property
    def imports(self) -> list['Injectable']:
        return self._imports()

    @property
    def products(self) -> list['Injectable']:
        return self._products()

    @property
    def import_resolved(self) -> bool:
        full_resolution: bool = all(
            implementation.is_resolved
            for implementation in self.imports
        )
        if full_resolution:
            return True
        if not self.needs_full_resolution:
            _logger.warning(f"Injectable {self.component_cls.__name__} is being resolved with unresolved imports: {[impl.component_cls.__name__ for impl in self.imports if not impl.is_resolved]}. This may lead to runtime errors if the provider relies on those imports. Consider declaring the dependencies as products or setting needs_full_resolution to True.")
        return False

    @property
    def provider(self) -> providers.Provider[Any]:
        """Return an instance from the provider."""
        if not self.is_resolved:
            raise DeclarationError(
                f"Injectable {self.component_cls.__name__} accessed before being resolved. "
                f"Ensure it is declared as a dependency (imports or products) where it is being used"
            )
        return self.provider_cls

    def inject(self) -> "Injectable":
        """Mark the injectable as resolved."""
        self.is_resolved = True
        return self

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
                f"Injectable {self.component_cls.__name__} must be resolved before initialization. "
                f"Ensure it is declared as a dependency (imports or products) where it is being used"
            )

        if self._bootstrap is not None:
            try:
                self._bootstrap()
            except CancelInitialization as e:
                _logger.warning(f"Injectable {self.component_cls.__name__} initialization skipped (cancelled by user): {e}")
            except Exception as e:
                raise InitializationError(f"Injectable {self.component_cls.__name__} initialization failed") from e

    def __repr__(self) -> str:
        return f"{self.component_cls.__name__}"
