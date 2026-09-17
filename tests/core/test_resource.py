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

    order = strategy.resolution(injectables, container)
    component: TComponent = TComponent.provide()
    assert component.initialized

    # `container.shutdown_resources()` reaches nothing here: plugin providers live in
    # sub-containers the root does not track (D-034). The framework walks the tree itself
    # now, in reverse resolution order (D-055).
    strategy.shutdown(providers=order)
    assert not component.initialized
    assert injectables == {TComponent.injection}


def test_entrypoint_shuts_its_own_resources_down() -> None:
    """The framework walks the tree; the application no longer has to (D-055)."""
    from dependency.core.agrupation import Entrypoint

    application = Entrypoint(container=Container(), plugins=[TPlugin])
    application.initialize()
    component: TComponent = TComponent.provide()
    assert component.initialized

    application.shutdown()

    assert not component.initialized
