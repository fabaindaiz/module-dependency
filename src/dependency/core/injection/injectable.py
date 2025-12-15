from typing import Any, Callable, Optional
from dependency_injector import containers, providers
from dependency.core.exceptions import CancelInitError

class Injectable:
    """Injectable Class representing a injectable dependency.
    """
    def __init__(self,
        component_cls: type,
        provided_cls: type,
        provider_cls: type[providers.Provider[Any]] = providers.Singleton,
        imports: list["Injectable"] = [],
        products: list["Injectable"] = [],
        bootstrap: Optional[Callable[[], Any]] = None
    ) -> None:
        self.component_cls: type = component_cls
        self.provided_cls: type = provided_cls
        self.provider_cls: type[providers.Provider[Any]] = provider_cls
        self.modules_cls: set[type] = {component_cls, provided_cls}
        self.imports: list["Injectable"] = imports
        self.products: list["Injectable"] = products
        self.bootstrap: Optional[Callable[[], Any]] = bootstrap
        self.is_resolved: bool = False

    @property
    def import_resolved(self) -> bool:
        return all(
            implementation.is_resolved
            for implementation in self.imports
        )

    def provider(self) -> providers.Provider[Any]:
        """Return an instance from the provider."""
        return self.provider_cls(self.provided_cls) # type: ignore

    def do_wiring(self, container: containers.DynamicContainer) -> "Injectable":
        """Wire the provider with the given container."""
        container.wire(modules=self.modules_cls)
        self.is_resolved = True
        return self

    # TODO: Permite definir una condición de inicialización en bootstrap
    def do_bootstrap(self) -> None:
        """Execute the bootstrap function if it exists."""
        if self.bootstrap is not None:
            try:
                self.bootstrap()
            except CancelInitError:
                pass

    def __repr__(self) -> str:
        return f"{self.provided_cls.__name__}"
