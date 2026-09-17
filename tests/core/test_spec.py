"""The frozen specs record what the decorator was given, and nothing else.

Nothing reads these yet. They exist so the graph can be built from declarations instead of
from mutated class attributes, and these tests are what pins their contents while the two
paths run side by side.
"""
from dependency_injector import providers
from dependency.core.agrupation import Plugin, PluginMeta, Module, module
from dependency.core.declaration import Component, component, instance, product
from dependency.core.injection.spec import (
    own_component_spec, own_implementation_spec, own_module_spec, target_component)

@module()
class SpecPlugin(Plugin):
    meta = PluginMeta(name="spec_plugin", version="0.1.0")

@module(
    module=SpecPlugin,
)
class SpecChildModule(Module):
    pass

@component(
    module=SpecPlugin,
)
class SpecDependency(Component):
    pass

@component(
    module=SpecPlugin,
)
class SpecOptionalDependency(Component):
    pass

@component(
    module=SpecChildModule,
    imports=[SpecDependency],
    optional=[SpecOptionalDependency],
    strict_resolution=False,
)
class SpecService(Component):
    pass

@instance(
    imports=[SpecDependency],
    provider=providers.Singleton,
    bootstrap=True,
)
class SpecServiceImpl(SpecService):
    pass

class SpecServiceSubclass(SpecServiceImpl):
    """Inherits the attribute through the MRO without having declared anything."""

@product(
    module=SpecPlugin,
)
class SpecProduct(Component):
    pass

def test_module_spec_records_the_root_flag() -> None:
    spec = own_module_spec(SpecPlugin)

    assert spec is not None
    assert spec.name == "SpecPlugin"
    assert spec.parent is None
    assert spec.is_root

def test_module_spec_records_its_parent_class() -> None:
    spec = own_module_spec(SpecChildModule)

    assert spec is not None
    assert spec.parent is SpecPlugin
    assert not spec.is_root

def test_component_spec_records_the_decorator_arguments() -> None:
    spec = own_component_spec(SpecService)

    assert spec is not None
    assert spec.module is SpecChildModule
    assert spec.imports == (SpecDependency,)
    assert spec.optional == (SpecOptionalDependency,)
    assert not spec.strict_resolution
    assert spec.provider_factory is None

def test_component_spec_without_a_provider_has_no_factory() -> None:
    spec = own_component_spec(SpecDependency)

    assert spec is not None
    assert spec.provider_factory is None
    assert spec.imports == ()

def test_implementation_spec_points_at_the_component_it_implements() -> None:
    spec = own_implementation_spec(SpecServiceImpl)

    assert spec is not None
    assert spec.target is SpecService
    assert spec.bootstrap

def test_implementation_spec_builds_a_new_provider_on_every_call() -> None:
    spec = own_implementation_spec(SpecServiceImpl)
    assert spec is not None

    first = spec.provider_factory(SpecServiceImpl)
    second = spec.provider_factory(SpecServiceImpl)

    assert isinstance(first, providers.Singleton)
    assert first is not second

def test_a_subclass_of_an_implementation_declares_nothing() -> None:
    assert own_implementation_spec(SpecServiceSubclass) is None
    assert hasattr(SpecServiceSubclass, "__implementation_spec__")

def test_product_declares_a_component_spec() -> None:
    spec = own_component_spec(SpecProduct)

    assert spec is not None
    assert spec.provider_factory is not None
    assert isinstance(spec.provider_factory(SpecProduct), providers.Factory)

def test_target_component_returns_none_when_no_base_declared_one() -> None:
    class SpecUndeclared:
        pass

    assert target_component(SpecUndeclared) is None
