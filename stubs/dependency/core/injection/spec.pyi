from _typeshed import Incomplete
from dataclasses import dataclass

ProviderFactory: Incomplete
MODULE_SPEC: str
COMPONENT_SPEC: str
IMPLEMENTATION_SPEC: str

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
    parent: type | None
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
    module: type | None
    imports: tuple[type, ...]
    optional: tuple[type, ...]
    strict_resolution: bool
    provider_factory: ProviderFactory | None
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
def own_module_spec(declared_cls: type) -> ModuleSpec | None:
    """The `ModuleSpec` this class declared itself, ignoring inherited ones."""
def own_component_spec(declared_cls: type) -> ComponentSpec | None:
    """The `ComponentSpec` this class declared itself, ignoring inherited ones."""
def own_implementation_spec(declared_cls: type) -> ImplementationSpec | None:
    """The `ImplementationSpec` this class declared itself, ignoring inherited ones.

    A subclass of an implementation inherits the attribute; only the class that carries it
    in its own `__dict__` declared it.
    """
def target_component(declared_cls: type) -> type | None:
    """The component an implementation implements: the nearest base that declared one.

    Args:
        declared_cls: The class decorated with `@instance`.

    Returns:
        Optional[type]: The component class, or None if no base declared one.
    """
