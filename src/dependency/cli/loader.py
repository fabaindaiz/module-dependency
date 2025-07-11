from jinja2 import Environment, PackageLoader, select_autoescape
from pydantic import BaseModel
from typing import Any

env = Environment(
    loader=PackageLoader(
        package_name="dependency.cli"),
    autoescape=select_autoescape(
        enabled_extensions=["j2"]
    )
)

class Module(BaseModel):
    name: str
    path: str

class Interface(BaseModel):
    name: str

class Component(BaseModel):
    name: str
    methods: list[str] = ["method"]

class Provider(BaseModel):
    name: str
    imports: list[Component] = []

def load_module(
        module: Module,
        ) -> str:
    variables: dict[str, Any] = {
        "module": module,
    }
    template = env.get_template("module.py.j2")
    return template.render(variables)

def load_component(
        module: Module,
        component: Component,
        ) -> str:
    variables: dict[str, Any] = {
        "component": component,
    }
    template = env.get_template("component.py.j2")
    return template.render(variables)

def load_provider(
        module: Module,
        component: Component,
        provider: Provider,
        ) -> str:
    variables: dict[str, Any] = {
        "module": module,
        "component": component,
        "provider": provider,
    }
    template = env.get_template("provider.py.j2")
    return template.render(variables)