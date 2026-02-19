import logging
from enum import Enum
from typing import Any, Callable, Iterable, Optional
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

        # Implementation details
        self.implementation: Optional[type] = None
        self.__provider: Optional[providers.Provider[Any]] = None
        self.__bootstrap: Optional[Callable[[], Any]] = None

        # Dependency tracking
        self.imports: set['Injectable'] = set()
        self.dependent: set['Injectable'] = set()

        # Validation flags
        self.partial_resolution: bool = False
        self.force_resolution: bool = False
        self.is_resolved: bool = False

    def check_resolved(self, providers: list['Injectable']) -> bool:
        if self.implementation is None:
            return False

        if self.force_resolution:
            self.is_resolved = True
            return True

        if self.partial_resolution:
            def validation(i: 'Injectable') -> bool:
                return i.is_resolved or i not in providers
        else:
            def validation(i: 'Injectable') -> bool:
                return i.is_resolved

        for provider in self.imports:
            if not validation(provider):
                return False

        self.is_resolved = True
        return True

    def update_dependencies(self,
        imports: Iterable['Injectable'],
        partial_resolution: Optional[bool] = None,
    ) -> None:
        self.imports.update(imports)
        for i in imports:
            i.dependent.add(self)

        if partial_resolution is not None:
            self.partial_resolution = partial_resolution

    def discard_dependencies(self,
        imports: Iterable['Injectable'],
    ) -> None:
        self.imports.difference_update(imports)
        for i in imports:
            i.dependent.discard(self)

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

        self.implementation = implementation
        self.modules_cls.update(modules_cls)
        self.__provider = provider
        self.__bootstrap = bootstrap

    @property
    def provider(self) -> providers.Provider[Any]:
        """Return the provider instance for this injectable."""
        if self.__provider is None:
            raise DeclarationError(f"Provider {self.interface_cls.__name__} has no implementation assigned")
        return self.__provider

    @property
    def provide(self) -> providers.Provider[Any]:
        """Return the provide instance for this injectable."""
        if not self.is_resolved:
            raise DeclarationError(
                f"Injectable {self.interface_cls.__name__} accessed before being resolved. "
                f"Ensure it is declared as a dependency (imports or products) where it is being used"
            )
        return self.provider

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

    def __hash__(self) -> int:
        return hash(self.interface_cls)

    def __repr__(self) -> str:
        return f"{self.interface_cls.__name__}"
