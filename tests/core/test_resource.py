from dependency.core.injection import ProviderInjection
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.declaration import Component, component, instance, providers
from dependency.core.resolution import Container, ResolutionStrategy


@module()
class TPlugin(Plugin):
    meta = PluginMeta(name="test_plugin", version="0.1.0")


@component(
    module=TPlugin,
)
class TComponent(Component):
    initialized: bool = False


@instance(
    provider=providers.Resource,
)
class TInstance(TComponent):
    def __enter__(self) -> "TInstance":
        self.initialized = True
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore
        self.initialized = False


def test_resource() -> None:
    strategy: ResolutionStrategy = ResolutionStrategy()
    container = Container()

    TPlugin.resolve_container(container)
    injectables: set[ProviderInjection] = set(TPlugin.collect_providers())
    assert not TInstance.initialized

    strategy.resolution(injectables, container)
    component: TComponent = TComponent.provide()
    assert component.initialized

    # TODO: Esto no está funcionando correctamente
    # container.shutdown_resources()
    TComponent.provider().shutdown()  # type: ignore
    assert not component.initialized
    assert injectables == {TComponent.injection}
