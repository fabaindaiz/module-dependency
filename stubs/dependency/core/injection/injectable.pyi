from typing import Any, Callable, Iterable

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
    interface_cls: type
    modules_cls: set[type]
    implementation: type | None
    bootstrap: Callable[[], Any] | None
    def __init__(self, interface_cls: type, implementation: type | None = None) -> None: ...
    def set_implementation(self, implementation: type, modules_cls: Iterable[type], bootstrap: Callable[[], Any] | None = None) -> None:
        """Assign a concrete implementation to this injectable.

        If an implementation was already assigned, logs a warning before
        overwriting — the last @instance decorator applied wins.
        """
