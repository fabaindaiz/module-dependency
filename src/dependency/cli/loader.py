from jinja2 import Environment, PackageLoader, select_autoescape
from pydantic import BaseModel
from typing import Any

env = Environment(
    loader=PackageLoader(
        package_name="dependency.cli"
    ),
    autoescape=select_autoescape(
        enabled_extensions=["j2"]
    )
)

class Imports(BaseModel):
    var: str
    name: str

class Component(BaseModel):
    name: str
    path: str

class Instance(BaseModel):
    name: str
    imports: list[Imports]

class Module(BaseModel):
    name: str
    path: str

def load_component(
        module: Module,
    ) -> str:
    variables: dict[str, Any] = {
        "module": module,
    }
    template = env.get_template("component.py.j2")
    return template.render(variables)

def load_instance(
        component: Component,
        instance: Instance,
    ) -> str:
    variables: dict[str, Any] = {
        "component": component,
        "instance": instance,
    }
    template = env.get_template("instance.py.j2")
    return template.render(variables)

def load_module(
        parent: Module,
        module: Module,
    ) -> str:
    variables: dict[str, Any] = {
        "parent": parent,
        "module": module,
    }
    template = env.get_template("module.py.j2")
    return template.render(variables)

def load_plugin(
        module: Module,
    ) -> str:
    variables: dict[str, Any] = {
        "module": module,
    }
    template = env.get_template("plugin.py.j2")
    return template.render(variables)