import logging
from typing import Any, Callable, Iterable, Self, Optional
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
    ) -> None:
        self.interface_cls: type = interface_cls
        self.modules_cls: set[type] = {interface_cls}

        self.implementation: Optional[type] = None
        self.__provider: Optional[providers.Provider[Any]] = None
        self.__bootstrap: Optional[Callable[[], Any]] = None

        self.__imports: set['Injectable'] = set()
        self.__products: set['Injectable'] = set()
        self.__import_of: set['Injectable'] = set()
        self.__product_of: set['Injectable'] = set()

        self.partial_resolution: bool = False
        self.is_resolved: bool = False

    @property
    def imports(self) -> Iterable['Injectable']:
        """Return the set of imports for this provider injection."""
        return self.__imports

    @property
    def products(self) -> Iterable['Injectable']:
        """Return the set of products for this provider injection."""
        return self.__products

    @property
    def import_resolved(self) -> bool:
        unresolved: set['Injectable'] = set(filter(lambda i: not i.is_resolved, self.__imports))
        if not unresolved:
            return True

        if self.partial_resolution:
            _logger.warning(f"Provider {self.interface_cls.__name__} has unresolved imports: {unresolved}, but partial resolution is enabled")
            return True

        return False

    def as_import(self, provider: 'Injectable') -> Self:
        self.__import_of.add(provider)
        return self

    def as_product(self, provider: 'Injectable') -> Self:
        self.__product_of.add(provider)
        return self

    def add_dependencies(self,
        imports: Iterable['Injectable'],
        products: Iterable['Injectable'],
        partial_resolution: bool = False,
    ) -> None:
        self.__imports.update(imports)
        self.__products.update(products)
        self.partial_resolution = partial_resolution

    def add_implementation(self,
        implementation: type,
        modules_cls: Iterable[type],
        provider: providers.Provider[Any],
        bootstrap: Optional[Callable[[], Any]] = None
    ) -> None:
        if self.implementation is None:
            _logger.debug(f"Provider {self.interface_cls.__name__} implementation assigned: {implementation.__name__}")
        else:
            _logger.warning(f"Provider {self.interface_cls.__name__} implementation reassigned: {self.implementation.__name__} -> {implementation.__name__}")

        self.modules_cls.update(modules_cls)
        self.implementation = implementation
        self.__provider = provider
        self.__bootstrap = bootstrap

    @property
    def injection(self) -> providers.Provider[Any]:
        """Return an instance from the provider."""
        if self.__provider is None:
            raise DeclarationError(f"Provider {self.interface_cls.__name__} has no implementation assigned")
        return self.__provider

    @property
    def provider(self) -> providers.Provider[Any]:
        """Return the provider instance for this injectable."""
        if not self.is_resolved:
            raise DeclarationError(
                f"Injectable {self.interface_cls.__name__} accessed before being resolved. "
                f"Ensure it is declared as a dependency (imports or products) where it is being used"
            )
        return self.injection

    def inject(self) -> Self:
        """Mark the provider injection as resolved."""
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
                f"Injectable {self.interface_cls.__name__} must be resolved before initialization. "
                f"Ensure it is declared as a dependency (imports or products) where it is being used"
            )

        if self.__bootstrap is not None:
            try:
                self.__bootstrap()
            except CancelInitialization as e:
                _logger.warning(f"Injectable {self.interface_cls.__name__} initialization skipped (cancelled by user): {e}")
            except Exception as e:
                raise InitializationError(f"Injectable {self.interface_cls.__name__} initialization failed") from e

    def __repr__(self) -> str:
        return f"{self.interface_cls.__name__}"
