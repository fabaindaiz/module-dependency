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
    strict_resolution: bool
    is_resolved: bool
    def __init__(self, interface_cls: type, implementation: type | None = None) -> None: ...
    def has_implementation(self) -> bool:
        """Check if the implementation of this injectable is valid.

        Returns:
            bool: True if the implementation is valid, False otherwise.
        """
    def resolve_if_posible(self, providers: set['Injectable']) -> bool:
        """Attempt to mark this injectable as resolved.

        Checks whether all imports are satisfied according to the resolution mode.
        In normal mode, all imports must already be resolved. In partial_resolution
        mode, an import is considered satisfied if it is resolved, also uses partial
        resolution, or is not part of the current provider set.

        If all imports are satisfied and an implementation is assigned, sets
        is_resolved=True as a side effect and returns True.

        Args:
            providers (set[Injectable]): The full set of injectables being resolved
                in the current resolution pass.

        Returns:
            bool: True if this injectable is now resolved, False otherwise.
        """
    def update_dependencies(self, imports: Iterable['Injectable'], partial_resolution: bool | None = None, strict_resolution: bool | None = None) -> None:
        """Add imports and update resolution flags.

        Registers the given injectables as dependencies of this injectable and
        records the reverse relationship (self as a dependent of each import).
        Resolution flags are updated only if explicitly provided (not None).

        Args:
            imports (Iterable[Injectable]): Injectables this injectable depends on.
            partial_resolution (bool, optional): If True, imports outside the current
                provider set are not required to be resolved.
            strict_resolution (bool, optional): If False, resolution proceeds even
                when no implementation has been assigned.
        """
    def discard_dependencies(self, imports: Iterable['Injectable']) -> None:
        """Remove imports from this injectable's dependency set.

        Removes the reverse dependent relationship from each discarded import as
        well. Useful when reconfiguring the dependency graph between resolution
        passes, for example in tests or dynamic reconfiguration scenarios.

        Args:
            imports (Iterable[Injectable]): Injectables to remove from imports.
        """
    def set_implementation(self, implementation: type, modules_cls: Iterable[type], bootstrap: Callable[[], Any] | None = None) -> None:
        """Assign a concrete implementation to this injectable.

        Sets the implementation class, adds its module to the wiring set, and
        optionally sets a bootstrap callable. If an implementation was already
        assigned, logs a warning before overwriting — the last @instance decorator
        applied to a given Component wins.

        Args:
            implementation (type): The concrete class implementing the interface.
            modules_cls (Iterable[type]): Modules to include in wiring for this
                implementation (typically the implementation class itself).
            bootstrap (Callable[[], Any], optional): Callable invoked during the
                initialization phase if bootstrap=True was set on the decorator.
        """
