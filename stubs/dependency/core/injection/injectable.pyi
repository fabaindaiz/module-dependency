from typing import Any, Callable, Iterable

class Injectable:
    """Injectable Class represents a implementation of some kind that can be injected as a dependency.

    Attributes:
        interface_cls (T): The interface class that this injectable implements.
    """
    interface_cls: type
    modules_cls: set[type]
    implementation: type | None
    bootstrap: Callable[[], Any] | None
    imports: set['Injectable']
    dependent: set['Injectable']
    partial_resolution: bool
    is_resolved: bool
    def __init__(self, interface_cls: type, implementation: type | None = None) -> None: ...
    def check_resolved(self, providers: list['Injectable']) -> bool: ...
    def update_dependencies(self, imports: Iterable['Injectable'], partial_resolution: bool | None = None) -> None: ...
    def discard_dependencies(self, imports: Iterable['Injectable']) -> None: ...
    def set_implementation(self, implementation: type, modules_cls: Iterable[type], bootstrap: Callable[[], Any] | None = None) -> None: ...
