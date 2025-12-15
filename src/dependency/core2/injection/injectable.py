from typing import Any, Callable, Optional, TypeVar
from dependency_injector import containers, providers

T = TypeVar('T')

class Injectable:
    def __init__(self,
        component_cls: type,
        provided_cls: type,
        provider_cls: type = providers.Singleton,
        imports: list["Injectable"] = [],
        bootstrap: Optional[Callable[[], Any]] = None
    ) -> None:
        self.component_cls: type = component_cls
        self.provided_cls: type = provided_cls
        self.provider_cls: type = provider_cls
        self.modules_cls: set[type] = {component_cls}
        self.imports: list["Injectable"] = imports
        self.bootstrap: Optional[Callable[[], Any]] = bootstrap

        self.is_resolved: bool = False

    @property
    def import_resolved(self) -> bool:
        return all(
            implementation.is_resolved
            for implementation in self.imports
        )

    def add_wire_cls(self, wire_cls: type) -> None:
        """Add a class to the set of modules that need to be wired."""
        self.modules_cls.add(wire_cls)

    def wire_provider(self, container: containers.DynamicContainer) -> "Injectable":
        container.wire(modules=self.modules_cls)
        self.is_resolved = True
        return self

    def provide(self) -> Any:
        return self.provider_cls(self.provided_cls)

    def prewiring(self) -> None:
        for implementation in self.imports:
            implementation.add_wire_cls(self.provided_cls)

    def do_bootstrap(self) -> None:
        if self.bootstrap is not None:
            self.bootstrap()

    def __hash__(self) -> int:
        return hash(self.component_cls)
