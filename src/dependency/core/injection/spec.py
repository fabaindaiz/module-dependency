"""Immutable declarations: what a decorator states, before anything is built.

A spec records the *arguments* of `@module`, `@component`, `@instance` and `@product`, and
nothing else. It is frozen, it holds tuples rather than sets, and — the load-bearing part —
it holds a **provider factory**, never a provider instance. A `providers.Singleton` built at
decoration time caches the object it builds, and that cache then outlives every rebuild of
the application; a factory is called once per build, so it cannot.

Specs live in `injection/` and not in `declaration/` on purpose. `declaration` may import
`injection`; the reverse would invert that edge and give `check_layering` a second cycle,
which is a failure rather than an advisory.

**Read a spec with the `own_*` helpers, never with `getattr`.** A subclass of an
implementation inherits `__implementation_spec__` through the MRO and would otherwise look
like a second declaration of the same thing.
"""

from dataclasses import dataclass
from typing import Any, Callable, Optional, cast
from dependency_injector import providers

ProviderFactory = Callable[[type], providers.Provider[Any]]

MODULE_SPEC = "__module_spec__"
COMPONENT_SPEC = "__component_spec__"
IMPLEMENTATION_SPEC = "__implementation_spec__"


@dataclass(frozen=True, slots=True)
class ModuleSpec:
    """What `@module` declared about a structural unit.

    Attributes:
        declared_cls: The decorated `Module` or `Plugin` class.
        name: The node name, which is the class name.
        parent: The parent `Module` class, or None for a root.
        provides: Component classes this module claims in the reverse direction.
        is_root: True when the decorated class is a `Plugin`.
    """

    declared_cls: type
    name: str
    parent: Optional[type]
    provides: tuple[type, ...]
    is_root: bool


@dataclass(frozen=True, slots=True)
class ComponentSpec:
    """What `@component` or `@product` declared about a providable unit.

    Attributes:
        declared_cls: The decorated `Component` class.
        name: The node name, which is the class name.
        module: The owning `Module` class, or None if it is declared elsewhere.
        imports: Required imports.
        optional: Optional imports, which never cascade a failure (D-003).
        strict_resolution: Whether a missing required import is reported (D-002).
        provider_factory: Set when the component provides itself inline.
        bootstrap: Whether this component is initialised at startup.
    """

    declared_cls: type
    name: str
    module: Optional[type]
    imports: tuple[type, ...]
    optional: tuple[type, ...]
    strict_resolution: bool
    provider_factory: Optional[ProviderFactory]
    bootstrap: bool


@dataclass(frozen=True, slots=True)
class ImplementationSpec:
    """What `@instance` declared about a concrete implementation.

    Attributes:
        declared_cls: The decorated implementation class.
        target: The `Component` class it implements, taken from the MRO.
        imports: Required imports.
        optional: Optional imports.
        strict_resolution: Whether a missing required import is reported.
        provider_factory: How to build this implementation's provider, per build.
        bootstrap: Whether this implementation is initialised at startup.
    """

    declared_cls: type
    target: type
    imports: tuple[type, ...]
    optional: tuple[type, ...]
    strict_resolution: bool
    provider_factory: ProviderFactory
    bootstrap: bool


def attach_spec(declared_cls: type, spec: object, attribute: str) -> None:
    """Attach a spec to the class that declared it.

    Args:
        declared_cls: The decorated class.
        spec: The frozen spec to record.
        attribute: One of `MODULE_SPEC`, `COMPONENT_SPEC`, `IMPLEMENTATION_SPEC`.
    """
    setattr(declared_cls, attribute, spec)


def own_module_spec(declared_cls: type) -> Optional[ModuleSpec]:
    """The `ModuleSpec` this class declared itself, ignoring inherited ones."""
    return cast(Optional[ModuleSpec], declared_cls.__dict__.get(MODULE_SPEC))


def own_component_spec(declared_cls: type) -> Optional[ComponentSpec]:
    """The `ComponentSpec` this class declared itself, ignoring inherited ones."""
    return cast(Optional[ComponentSpec], declared_cls.__dict__.get(COMPONENT_SPEC))


def own_implementation_spec(declared_cls: type) -> Optional[ImplementationSpec]:
    """The `ImplementationSpec` this class declared itself, ignoring inherited ones.

    A subclass of an implementation inherits the attribute; only the class that carries it
    in its own `__dict__` declared it.
    """
    return cast(
        Optional[ImplementationSpec], declared_cls.__dict__.get(IMPLEMENTATION_SPEC)
    )


def target_component(declared_cls: type) -> Optional[type]:
    """The component an implementation implements: the nearest base that declared one.

    Args:
        declared_cls: The class decorated with `@instance`.

    Returns:
        Optional[type]: The component class, or None if no base declared one.
    """
    for base in declared_cls.__mro__[1:]:
        if own_component_spec(base) is not None:
            return base
    return None
