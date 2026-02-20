import logging
from typing import Any, Callable, Iterable, Optional
_logger = logging.getLogger("dependency.loader")

class Injectable:
    """Injectable Class represents a implementation of some kind that can be injected as a dependency.

    Attributes:
        interface_cls (T): The interface class that this injectable implements.
    """
    def __init__(self,
        interface_cls: type,
        implementation: Optional[type] = None,
    ) -> None:
        self.interface_cls: type = interface_cls
        self.modules_cls: set[type] = {interface_cls}

        # Implementation details
        self.implementation: Optional[type] = implementation
        self.bootstrap: Optional[Callable[[], Any]] = None

        # Dependency tracking
        self.imports: set['Injectable'] = set()
        self.dependent: set['Injectable'] = set()

        # Validation flags
        self.partial_resolution: bool = False
        self.is_resolved: bool = False

    def check_resolved(self, providers: list['Injectable']) -> bool:
        if self.implementation is None:
            return False

        if self.partial_resolution:
            def validation(i: 'Injectable') -> bool:
                return (
                    i.is_resolved or
                    i.partial_resolution or
                    i not in providers
                )
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

    def set_implementation(self,
        implementation: type,
        modules_cls: Iterable[type],
        bootstrap: Optional[Callable[[], Any]] = None
    ) -> None:
        if self.implementation is None:
            _logger.debug(f"Provider {self.interface_cls.__name__} implementation assigned: {implementation.__name__}")
        else:
            _logger.warning(f"Provider {self.interface_cls.__name__} implementation reassigned: {self.implementation.__name__} -> {implementation.__name__}")

        self.implementation = implementation
        self.modules_cls.update(modules_cls)
        self.bootstrap = bootstrap

    def __repr__(self) -> str:
        return f"{self.interface_cls.__name__}"
