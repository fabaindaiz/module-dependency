from dependency_injector import containers, providers
from typing import Any, Callable, Optional, TypeVar

T = TypeVar('T')

class Implementation():
    def __init__(self,
        provider_cls: type,
        provided_cls: type,
        component_cls: type,
        imports: list["Implementation"] = [],
        bootstrap: Optional[Callable[[], Any]] = None
    ) -> None:
        self.provider_cls: type = provider_cls
        self.provided_cls: type = provided_cls
        self.modules_cls: set[type] = {component_cls}
        self.imports: list["Implementation"] = imports
        self.bootstrap: Optional[Callable[[], Any]] = bootstrap

    def add_wire_cls(self, wire_cls: type) -> None:
        """Add a class to the set of modules that need to be wired."""
        self.modules_cls.add(wire_cls)

    def wire_provider(self, container: containers.DynamicContainer) -> "Implementation":
        container.wire(modules=self.modules_cls)
        return self

    def provide(self) -> Any:
        return self.provider_cls(self.provided_cls)

    def prewiring(self) -> None:
        for implementation in self.imports:
            implementation.add_wire_cls(self.provided_cls)

    def do_bootstrap(self) -> None:
        if self.bootstrap is not None:
            self.bootstrap()
