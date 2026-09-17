"""The `dependency` command.

Two jobs, and the second is the one only this framework can do:

- **Scaffold** — `new plugin|module|component|instance`, the four generators that already
  existed and that nothing could invoke, because no console entry point was declared.
- **Answer whether a graph holds, without starting the application** — `check`, `show` and
  `graph`. The invariant is that the whole graph is validated before the first user object
  is constructed (D-001); these expose that answer to a shell, a CI job or a pre-commit
  hook, and never run wiring or bootstrap.

`argparse` on purpose: a CLI that adds a dependency to a dependency-injection library is a
poor trade, and the surface here does not need more.
"""

from typing import Optional, Sequence
import argparse
import json
import sys

from dependency.cli.generation.component import ComponentGenerator
from dependency.cli.generation.instance import InstanceGenerator
from dependency.cli.generation.module import ModuleGenerator
from dependency.cli.generation.plugin import PluginGenerator
from dependency.cli.inspection import (
    EntrypointError,
    describe,
    expand,
    import_modules,
    load_plugins,
)
from dependency.cli.models.base import Component, Instance, Module
from dependency.core.exceptions import DependencyError

PROGRAM = "dependency"
ENTRYPOINT_HELP = "the plugins to load, as 'package.module:ATTRIBUTE'"
IMPORT_HELP = (
    "a module to import for its registration side effect; repeatable. Without these the "
    "@instance declarations never run and every component looks unimplemented"
)


def _split_reference(value: str, flag: str) -> Module:
    """Turn `package.module:Name` into the path/name pair the templates expect."""
    if ":" not in value:
        raise argparse.ArgumentTypeError(
            f"{flag} expects 'package.module:Name', got {value!r}"
        )
    path, _, name = value.partition(":")
    return Module(path=path, name=name)


def _write(text: str, output: Optional[str]) -> None:
    """Write generated source to a file, or to stdout when no file was named."""
    if output is None:
        print(text)
        return
    with open(output, "w", encoding="utf-8") as handle:
        handle.write(text if text.endswith("\n") else text + "\n")
    print(f"wrote {output}", file=sys.stderr)


def _load(arguments: argparse.Namespace) -> list[type]:
    """Import the registration modules, then resolve the entrypoint spec."""
    import_modules(arguments.imports or ())
    return load_plugins(arguments.entrypoint)


def _config(arguments: argparse.Namespace) -> dict[str, object]:
    """Read the application configuration a plugin's `config:` hint will be validated against."""
    if not arguments.config:
        return {}
    with open(arguments.config, encoding="utf-8") as handle:
        loaded: dict[str, object] = json.load(handle)
    return loaded


def _add_entrypoint_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("entrypoint", help=ENTRYPOINT_HELP)
    parser.add_argument("-i", "--import", dest="imports", action="append", metavar="MODULE", help=IMPORT_HELP)
    parser.add_argument("-c", "--config", metavar="FILE", help="a JSON configuration file for the container")


def build_parser() -> argparse.ArgumentParser:
    """The whole command surface, in one place."""
    parser = argparse.ArgumentParser(
        prog=PROGRAM,
        description="Scaffold and inspect applications built with module-dependency.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    new = commands.add_parser("new", help="generate a plugin, module, component or instance")
    kinds = new.add_subparsers(dest="kind", required=True)

    for kind, helptext in (
        ("plugin", "a root Plugin with its config model"),
        ("module", "a Module nested under a parent"),
        ("component", "a Component interface and its declaration"),
        ("instance", "an implementation of an existing Component"),
    ):
        sub = kinds.add_parser(kind, help=helptext)
        sub.add_argument("name", help="the class name to generate")
        sub.add_argument("-o", "--output", metavar="FILE", help="write here instead of stdout")
        if kind == "module":
            sub.add_argument("--parent", required=True, metavar="package.module:Name",
                             help="the module this one nests under")
        if kind == "component":
            sub.add_argument("--module", required=True, metavar="package.module:Name",
                             help="the module that owns this component")
            sub.add_argument("--interface", metavar="NAME",
                             help="the abstract interface name (default: <Name>Interface)")
        if kind == "instance":
            sub.add_argument("--component", required=True, metavar="package.module:Name",
                             help="the component this implements")
            sub.add_argument("--imports", metavar="A,B", default="",
                             help="comma-separated components to inject")

    check = commands.add_parser(
        "check", help="expand the graph and fail if it cannot be satisfied")
    _add_entrypoint_arguments(check)

    show = commands.add_parser("show", help="print the resolved injection tree")
    _add_entrypoint_arguments(show)

    graph = commands.add_parser("graph", help="render the injection tree to SVG (needs the [graph] extra)")
    _add_entrypoint_arguments(graph)
    graph.add_argument("-o", "--output", default="build/graph", metavar="PATH",
                       help="output path without extension (default: build/graph)")

    commands.add_parser("version", help="print the installed version")
    return parser


def _run_new(arguments: argparse.Namespace) -> int:
    if arguments.kind == "plugin":
        _write(PluginGenerator.generate(module=Module(path="", name=arguments.name)), arguments.output)
    elif arguments.kind == "module":
        _write(ModuleGenerator.generate(
            parent=_split_reference(arguments.parent, "--parent"),
            module=Module(path="", name=arguments.name),
        ), arguments.output)
    elif arguments.kind == "component":
        _write(ComponentGenerator.generate(
            component=Component(
                path="",
                name=arguments.name,
                interface=arguments.interface or f"{arguments.name}Interface",
            ),
            module=_split_reference(arguments.module, "--module"),
        ), arguments.output)
    else:
        component = _split_reference(arguments.component, "--component")
        _write(InstanceGenerator.generate(
            component=Component(path=component.path, name=component.name, interface=component.name),
            instance=Instance(
                path="",
                name=arguments.name,
                imports=[part.strip() for part in arguments.imports.split(",") if part.strip()],
            ),
        ), arguments.output)
    return 0


NOTHING_REGISTERED = (
    "no provider resolved from {count} plugin(s). A component with no implementation is "
    "not an error on its own (D-002), so an empty graph expands cleanly and proves "
    "nothing. The usual cause is that no implementation was registered: pass --import for "
    "each module whose @instance declarations should run, the way an imports.py does."
)


def _run_check(arguments: argparse.Namespace) -> int:
    plugins = _load(arguments)
    providers = expand(plugins, _config(arguments))
    if not providers:
        print(f"{PROGRAM}: " + NOTHING_REGISTERED.format(count=len(plugins)), file=sys.stderr)
        return 1
    print(f"{len(providers)} provider(s) resolved across {len(plugins)} plugin(s)")
    return 0


def _run_show(arguments: argparse.Namespace) -> int:
    plugins = _load(arguments)
    expand(plugins, _config(arguments))
    for line in describe(plugins):
        print(line)
    return 0


def _run_graph(arguments: argparse.Namespace) -> int:
    from dependency.library.graph import generate_graph

    plugins = _load(arguments)
    expand(plugins, _config(arguments))
    generate_graph(plugins, output=arguments.output)
    print(f"wrote {arguments.output}.svg")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point for the `dependency` console script.

    Returns:
        int: 0 on success, 1 on a graph or entrypoint failure, 2 on a usage error.
    """
    arguments = build_parser().parse_args(argv)
    handlers = {
        "new": _run_new,
        "check": _run_check,
        "show": _run_show,
        "graph": _run_graph,
    }
    if arguments.command == "version":
        from importlib.metadata import version

        print(version("module-dependency"))
        return 0
    try:
        return handlers[arguments.command](arguments)
    except (EntrypointError, DependencyError) as failure:
        print(f"{PROGRAM}: {failure}", file=sys.stderr)
        return 1
    except ImportError as failure:
        print(f"{PROGRAM}: {failure}", file=sys.stderr)
        return 1
    except OSError as failure:
        print(f"{PROGRAM}: {failure}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as failure:
        print(f"{PROGRAM}: {arguments.config}: {failure}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
