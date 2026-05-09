from dependency.core.agrupation import Plugin, PluginMeta, Module, module
from dependency.core.declaration import Component, component, instance
from dependency.core.resolution import Container, InjectionResolver

@module()
class TPlugin(Plugin):
    meta = PluginMeta(name="test_provides_plugin", version="0.1.0")

@component()
class TService(Component):
    pass

@instance()
class TServiceImpl(TService):
    pass

@module(
    module=TPlugin,
    provides=[TService],
)
class TModule(Module):
    pass


def test_provides_assigns_parent() -> None:
    """provides= asigna el módulo como padre del componente."""
    assert TService.injection.parent == TModule.injection
    assert TService.injection in TModule.injection.childs

def test_provides_reference() -> None:
    """El reference del componente refleja el módulo asignado via provides=."""
    assert TService.injection.reference == "TPlugin.TModule.TService"

def test_provides_resolves() -> None:
    """Un componente declarado via provides= entra al proceso de resolución y se resuelve."""
    container = Container()
    TPlugin.inject_container(container)
    loader = InjectionResolver(container=container)
    providers = loader.resolve_injectables(modules=[TPlugin])
    assert TService.injection in providers
    loader.resolve_providers(providers=providers)
    assert TService.injection.is_resolved

def test_provides_equivalent_to_module_param() -> None:
    """provides=[X] en @module es equivalente a module=M en @component."""
    assert TService.injection.parent == TModule.injection
