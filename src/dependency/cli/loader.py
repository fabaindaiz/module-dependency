from jinja2 import Environment, PackageLoader, select_autoescape
from dependency.cli.base import Module, Component, Instance

env = Environment(
    loader=PackageLoader(
        package_name="dependency.cli",
        package_path="templates",
    ),
    autoescape=select_autoescape(
        enabled_extensions=["j2"]
    )
)

def load_plugin(
        module: Module,
    ) -> str:
    template = env.get_template("plugin.py.j2")
    return template.render(
        module=module,
    )

def load_module(
        parent: Module,
        module: Module,
    ) -> str:
    template = env.get_template("module.py.j2")
    return template.render(
        parent=parent,
        module=module,
    )

def load_component(
        component: Component,
        module: Module,
    ) -> str:
    template = env.get_template("component.py.j2")
    return template.render(
        component=component,
        module=module,
    )

def load_instance(
        component: Component,
        instance: Instance,
    ) -> str:
    template = env.get_template("instance.py.j2")
    return template.render(
        component=component,
        instance=instance,
    )