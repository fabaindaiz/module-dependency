import argparse
from dependency.cli.generation.component import ComponentGenerator as ComponentGenerator
from dependency.cli.generation.instance import InstanceGenerator as InstanceGenerator
from dependency.cli.generation.module import ModuleGenerator as ModuleGenerator
from dependency.cli.generation.plugin import PluginGenerator as PluginGenerator
from dependency.cli.inspection import EntrypointError as EntrypointError, describe as describe, expand as expand, import_modules as import_modules, load_plugins as load_plugins
from dependency.cli.models.base import Component as Component, Instance as Instance, Module as Module
from dependency.core.exceptions import DependencyError as DependencyError
from typing import Sequence

PROGRAM: str
ENTRYPOINT_HELP: str
IMPORT_HELP: str

def build_parser() -> argparse.ArgumentParser:
    """The whole command surface, in one place."""

NOTHING_REGISTERED: str

def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for the `dependency` console script.

    Returns:
        int: 0 on success, 1 on a graph or entrypoint failure, 2 on a usage error.
    """
