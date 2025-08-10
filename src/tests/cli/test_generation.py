from dependency.cli.base import Module, Component, Instance
import dependency.cli.loader as loader

def test_generation():
    plugin = Module(
        path="src.plugin",
        name="Plugin",
    )
    module = Module(
        path="src.plugin.module",
        name="Module",
    )
    component = Component(
        path="src.plugin.module.component",
        name="Component",
        interface="Interface",
    )
    instance = Instance(
        path="src.plugin.module.component.instance",
        name="ComponentA",
        imports=["Component"],
    )
    
    loader.load_plugin(
        module=plugin,
    )
    loader.load_module(
        parent=plugin,
        module=module,
    )
    loader.load_component(
        component=component,
        module=module,
    )
    loader.load_instance(
        component=component,
        instance=instance,
    )