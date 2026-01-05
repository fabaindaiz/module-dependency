import pytest
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.declaration import Component, component, Product, product, instance
from dependency.core.resolution import Container, InjectionResolver
from dependency.core.exceptions import DeclarationError, ResolutionError

@module()
class TPlugin(Plugin):
    meta = PluginMeta(name="test_plugin", version="0.1.0")

class TInterface:
    pass

@component(
    module=TPlugin,
    interface=TInterface,
)
class TComponent1(Component):
    pass

@component(
    interface=TInterface,
)
class TComponent2(Component):
    pass

@product(
    imports=[
        TComponent1,
        TComponent2,
    ],
)
class TProduct1(Product):
    pass

@instance(
    component=TComponent1,
    imports=[TComponent2],
    products=[TProduct1],
)
class TInstance1(TInterface):
    pass

def test_products():
    container = Container()
    TPlugin.resolve_container(container)
    providers = TPlugin.resolve_providers()
    loader = InjectionResolver(container, providers)

    # TODO: Implement unresolved products policy
    with pytest.raises(DeclarationError):
        loader.resolve_injectables()
