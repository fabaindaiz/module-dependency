import logging
from typing import Any, Callable, Iterable, Optional
_logger = logging.getLogger("dependency.loader")

class Injectable:
    """Binding between a Component interface and its concrete implementation.

    Created at @component decoration time. The implementation is assigned later
    by @instance when the concrete class is declared separately.

    Attributes:
        interface_cls: The interface class (the decorated Component).
        implementation: The concrete class assigned by @instance, if any.
        modules_cls: Python modules to include in dependency-injector wiring.
        bootstrap: Callable invoked during initialization if bootstrap=True.
    """
    def __init__(self,
        interface_cls: type,
        implementation: Optional[type] = None,
    ) -> None:
        self.interface_cls: type = interface_cls
        self.modules_cls: set[type] = {interface_cls}
        self.implementation: Optional[type] = implementation
        self.bootstrap: Optional[Callable[[], Any]] = None

    def set_implementation(self,
        implementation: type,
        modules_cls: Iterable[type],
        bootstrap: Optional[Callable[[], Any]] = None,
    ) -> None:
        """Assign a concrete implementation to this injectable.

        If an implementation was already assigned, logs a warning before
        overwriting — the last @instance decorator applied wins.
        """
        if self.implementation is None:
            _logger.debug(f"Provider {self.interface_cls.__name__} implementation assigned: {implementation.__name__}")
        else:
            _logger.warning(f"Provider {self.interface_cls.__name__} implementation reassigned: {self.implementation.__name__} -> {implementation.__name__}")

        self.implementation = implementation
        self.modules_cls.update(modules_cls)
        self.bootstrap = bootstrap

    def __repr__(self) -> str:
        return f"{self.interface_cls.__name__}"
