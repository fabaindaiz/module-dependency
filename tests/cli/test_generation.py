"""The generators must emit source that parses and declares what was asked for.

This file used to call all four generators and assert nothing, so it passed while the
templates emitted keywords no decorator accepted. `tests/CLAUDE.md` recorded that as a
known gap: a generator test must execute or at least `ast.parse` and inspect what it
rendered, never merely render it.
"""

import ast

from dependency.cli.generation.component import ComponentGenerator
from dependency.cli.generation.instance import InstanceGenerator
from dependency.cli.generation.module import ModuleGenerator
from dependency.cli.generation.plugin import PluginGenerator
from dependency.cli.models.base import Component, Instance, Module

PLUGIN = Module(path="src.plugin", name="Plugin")
MODULE = Module(path="src.plugin.module", name="Module")
COMPONENT = Component(path="src.plugin.module.component", name="Component", interface="Interface")
INSTANCE = Instance(path="src.plugin.module.component.instance", name="ComponentA", imports=["Component"])


def _classes(source: str) -> dict[str, ast.ClassDef]:
    return {
        node.name: node
        for node in ast.parse(source).body
        if isinstance(node, ast.ClassDef)
    }


def _decorator_keywords(node: ast.ClassDef) -> set[str]:
    return {
        keyword.arg
        for decorator in node.decorator_list
        if isinstance(decorator, ast.Call)
        for keyword in decorator.keywords
        if keyword.arg is not None
    }


def test_plugin_declares_a_plugin_and_its_config_model() -> None:
    classes = _classes(PluginGenerator.generate(module=PLUGIN))

    assert set(classes) == {"PluginConfig", "Plugin"}
    assert [base.id for base in classes["Plugin"].bases if isinstance(base, ast.Name)] == ["Plugin"]
    assert _decorator_keywords(classes["Plugin"]) == set()


def test_module_nests_under_the_parent_it_was_given() -> None:
    source = ModuleGenerator.generate(parent=PLUGIN, module=MODULE)
    classes = _classes(source)

    assert _decorator_keywords(classes["Module"]) == {"module"}
    assert f"from {PLUGIN.path} import {PLUGIN.name}" in source


def test_component_emits_an_interface_and_a_declaration() -> None:
    source = ComponentGenerator.generate(component=COMPONENT, module=MODULE)
    classes = _classes(source)

    assert "Interface" in classes
    assert [base.id for base in classes["Component"].bases if isinstance(base, ast.Name)] == [
        "Interface",
        "Component",
    ]
    assert _decorator_keywords(classes["Component"]) == {"module"}


def test_instance_injects_every_declared_import() -> None:
    source = InstanceGenerator.generate(component=COMPONENT, instance=INSTANCE)
    classes = _classes(source)

    assert _decorator_keywords(classes["ComponentA"]) == {"imports", "provider"}
    assert "Component.provide()" in source


def test_every_generator_emits_parseable_source() -> None:
    for source in (
        PluginGenerator.generate(module=PLUGIN),
        ModuleGenerator.generate(parent=PLUGIN, module=MODULE),
        ComponentGenerator.generate(component=COMPONENT, module=MODULE),
        InstanceGenerator.generate(component=COMPONENT, instance=INSTANCE),
    ):
        compile(source, "<generated>", "exec")
