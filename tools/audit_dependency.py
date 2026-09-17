"""Check the repository against the rules it writes down about itself.

Every rule below is written in CLAUDE.md, an <area>/CLAUDE.md, or docs/architecture.md.
If a rule changes there, change it here too; if a check here has no rule, it should not
be failing the build.

Two severities:
  FAILURE   stops the build.
  ADVISORY  is printed every run and stops nothing. A rule goes here when its legitimate
            exceptions are real -- an accepted architectural cycle is a decision, letting
            a third one appear is not.

Run: hatch run build:audit
"""

from __future__ import annotations

import ast
import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from importlib.metadata import packages_distributions
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "dependency"
STUBS = ROOT / "stubs" / "dependency"
DOCS = ROOT / "docs"
SNAPSHOT = ROOT / "tools" / "api_snapshot.json"


@dataclass
class Report:
    failures: list[str] = field(default_factory=list)
    advisories: list[str] = field(default_factory=list)
    checks_run: int = 0

    def fail(self, check: str, message: str) -> None:
        self.failures.append(f"[{check}] {message}")

    def advise(self, check: str, message: str) -> None:
        self.advisories.append(f"[{check}] {message}")


def pyproject() -> dict:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        return tomllib.load(fh)


def source_files() -> list[Path]:
    return sorted(p for p in SRC.rglob("*.py") if "__pycache__" not in p.parts)


# ---------------------------------------------------------------- version floor

def check_version_floor(report: Report) -> None:
    """requires-python, the mypy python_version and CI must name the same floor.

    Rule: CLAUDE.md, "Packaging and compatibility". Three places disagreed once and the
    package shipped claiming a Python it could not import on.
    """
    data = pyproject()
    declared = data["project"].get("requires-python", "")
    match = re.search(r"(\d+)\.(\d+)", declared)
    if not match:
        report.fail("version_floor", f"cannot parse requires-python: {declared!r}")
        return
    floor = f"{match.group(1)}.{match.group(2)}"

    mypy_ini = ROOT / ".mypy.ini"
    if mypy_ini.exists():
        found = re.search(r"python_version\s*=\s*([\d.]+)", mypy_ini.read_text())
        if found and found.group(1) != floor:
            report.fail(
                "version_floor",
                f".mypy.ini python_version={found.group(1)} but requires-python floor is {floor}",
            )

    for workflow in sorted((ROOT / ".github" / "workflows").glob("*.y*ml")):
        for version in re.findall(r"python-version:\s*['\"]?([\d.]+)", workflow.read_text()):
            if tuple(map(int, version.split("."))) < tuple(map(int, floor.split("."))):
                report.fail(
                    "version_floor",
                    f"{workflow.name} runs Python {version}, below the declared floor {floor}",
                )


# ------------------------------------------------------------- forward refs

def check_forward_refs(report: Report) -> None:
    """Unquoted class-body annotations must not name something defined later.

    PEP 649 makes these work on 3.14 only; on 3.12 and 3.13 they raise NameError at
    import. Rule: CLAUDE.md, "Packaging and compatibility".
    """
    for path in source_files():
        tree = ast.parse(path.read_text(), filename=str(path))
        if any(
            isinstance(node, ast.ImportFrom)
            and node.module == "__future__"
            and any(alias.name == "annotations" for alias in node.names)
            for node in tree.body
        ):
            continue

        defined_at: dict[str, int] = {}
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                defined_at[node.name] = node.lineno
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_at[target.id] = node.lineno

        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            for stmt in node.body:
                if not isinstance(stmt, ast.AnnAssign) or stmt.annotation is None:
                    continue
                for name in ast.walk(stmt.annotation):
                    if not isinstance(name, ast.Name):
                        continue
                    later = defined_at.get(name.id)
                    if later is not None and later > node.lineno:
                        report.fail(
                            "forward_refs",
                            f"{path.relative_to(ROOT)}:{stmt.lineno} annotation names "
                            f"{name.id!r}, defined later at line {later}. Quote it, reorder "
                            f"the classes, or add `from __future__ import annotations`.",
                        )


# --------------------------------------------------------- declared imports

def check_declared_imports(report: Report) -> None:
    """Every third-party import must be a declared dependency or a declared extra.

    An undeclared import works from the source tree and fails on the user's machine.
    Rule: CLAUDE.md, "Packaging and compatibility"; src/dependency/library/CLAUDE.md.
    """
    data = pyproject()

    def normalise(spec: str) -> str:
        return re.split(r"[<>=!\[;\s]", spec, maxsplit=1)[0].strip().replace("_", "-").lower()

    declared = {normalise(d) for d in data["project"].get("dependencies", [])}
    for extra_deps in data["project"].get("optional-dependencies", {}).values():
        declared |= {normalise(d) for d in extra_deps}

    mapping = packages_distributions()
    stdlib = sys.stdlib_module_names

    for path in source_files():
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots = [node.module.split(".")[0]]
            else:
                continue
            for root in roots:
                if root in stdlib or root == "dependency":
                    continue
                dists = {d.replace("_", "-").lower() for d in mapping.get(root, [])}
                if not dists:
                    report.advise(
                        "declared_imports",
                        f"{path.relative_to(ROOT)}: cannot map import {root!r} to a "
                        f"distribution (not installed?)",
                    )
                elif not (dists & declared):
                    report.fail(
                        "declared_imports",
                        f"{path.relative_to(ROOT)}:{node.lineno} imports {root!r} "
                        f"({'/'.join(sorted(dists))}) which is not in [project.dependencies] "
                        f"nor in any declared extra",
                    )


# --------------------------------------------------------------- stub parity

def check_stub_parity(report: Report) -> None:
    """Every published module needs a stub: the stubs are the only type surface.

    PEP 561 ranks `-stubs` packages above inline annotations and this package ships no
    py.typed. Rule: CLAUDE.md, "Packaging and compatibility".
    """
    expected = {p.relative_to(SRC).with_suffix("") for p in source_files()}
    actual = {
        p.relative_to(STUBS).with_suffix("")
        for p in STUBS.rglob("*.pyi")
        if "__pycache__" not in p.parts
    }
    for missing in sorted(expected - actual):
        report.fail("stub_parity", f"no stub for dependency/{missing}.py — run `hatch run build:stubs`")
    for orphan in sorted(actual - expected):
        report.fail("stub_parity", f"stub dependency-stubs/{orphan}.pyi has no source module")


# ----------------------------------------------------------- docs references

def check_docs_references(report: Report) -> None:
    """Every `::: dotted.path` in docs/reference/ must resolve to a real module.

    mkdocs runs with strict: true, so a dead reference fails the release docs job.
    Rule: CLAUDE.md, document map.
    """
    for page in sorted((DOCS / "reference").glob("*.md")):
        for line in page.read_text().splitlines():
            match = re.match(r"^:::\s+([\w.]+)", line.strip())
            if not match:
                continue
            dotted = match.group(1)
            if not dotted.startswith("dependency."):
                continue
            relative = Path(*dotted.split(".")[1:])
            if not ((SRC / relative).with_suffix(".py").exists() or (SRC / relative).is_dir()):
                report.fail(
                    "docs_references",
                    f"{page.relative_to(ROOT)} points at {dotted}, which does not exist",
                )


# -------------------------------------------------------------- document map

def check_document_map(report: Report) -> None:
    """Every document named in a CLAUDE.md must exist. A dead pointer is worse than none."""
    pattern = re.compile(r"`((?:docs|\.claude|src|tests)[\w/.\-]*\.md)`")
    for claude in sorted(ROOT.rglob("CLAUDE.md")):
        if ".claude" in claude.parts:
            continue
        for referenced in set(pattern.findall(claude.read_text())):
            if not (ROOT / referenced).exists():
                report.fail(
                    "document_map",
                    f"{claude.relative_to(ROOT)} points at {referenced}, which does not exist",
                )


# ------------------------------------------------------------- cli templates

def check_cli_templates(report: Report) -> None:
    """A template may only emit decorator keywords that exist in the live signature.

    Generated code that raises TypeError on import is worse than no generator.
    Rule: src/dependency/cli/CLAUDE.md.
    """
    import inspect

    try:
        from dependency.cli.generation.component import ComponentGenerator
        from dependency.cli.generation.instance import InstanceGenerator
        from dependency.cli.generation.module import ModuleGenerator
        from dependency.cli.generation.plugin import PluginGenerator
        from dependency.cli.models.base import Component, Instance, Module
        from dependency.core import component, instance, module, product
    except ImportError as exc:  # pragma: no cover
        report.advise("cli_templates", f"cannot import the CLI package: {exc}")
        return

    decorators = {"component": component, "instance": instance, "module": module, "product": product}

    sample_module = Module(path="pkg.plugin", name="SamplePlugin")
    sample_component = Component(path="pkg.plugin.svc", name="SampleComponent", interface="SampleInterface")
    sample_instance = Instance(path="pkg.plugin.svc.impl", name="SampleImpl", imports=["SampleComponent"])

    rendered = {
        "plugin.py.j2": PluginGenerator.generate(module=sample_module),
        "module.py.j2": ModuleGenerator.generate(parent=sample_module, module=sample_module),
        "component.py.j2": ComponentGenerator.generate(component=sample_component, module=sample_module),
        "instance.py.j2": InstanceGenerator.generate(component=sample_component, instance=sample_instance),
    }

    for name, source in rendered.items():
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            report.fail("cli_templates", f"{name} renders invalid Python: {exc}")
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            for decorator in node.decorator_list:
                if not (isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name)):
                    continue
                target = decorators.get(decorator.func.id)
                if target is None:
                    continue
                allowed = set(inspect.signature(target).parameters)
                for keyword in decorator.keywords:
                    if keyword.arg and keyword.arg not in allowed:
                        report.fail(
                            "cli_templates",
                            f"{name} emits @{decorator.func.id}({keyword.arg}=...) but "
                            f"{decorator.func.id}() accepts only {sorted(allowed)}",
                        )


# ---------------------------------------------------------------- changelog

def check_changelog_version(report: Report) -> None:
    """The version in pyproject.toml must have a CHANGELOG entry.

    Rule: CLAUDE.md, "Logging obligation". Two releases shipped with no entry.
    """
    version = pyproject()["project"]["version"]
    changelog = (ROOT / "CHANGELOG.md").read_text()
    if not re.search(rf"^##\s*\[?v?{re.escape(version)}\]?", changelog, re.MULTILINE):
        report.fail(
            "changelog",
            f"pyproject version {version} has no CHANGELOG.md entry",
        )


# ------------------------------------------------------------- hatch scripts

def check_hatch_scripts(report: Report) -> None:
    """A `python <file>` script must point at a file that exists and calls real arity.

    Rule: CLAUDE.md, "Commands". `hatch run build:graph` shipped calling
    generate_graph() with no arguments against a one-required-argument signature.
    """
    import inspect
    import importlib

    envs = pyproject().get("tool", {}).get("hatch", {}).get("envs", {})
    for env_name, env in envs.items():
        for script_name, command in env.get("scripts", {}).items():
            if not isinstance(command, str):
                continue
            match = re.match(r"python\s+(\S+\.py)$", command.strip())
            if not match:
                continue
            script = ROOT / match.group(1)
            if not script.exists():
                report.fail("hatch_scripts", f"{env_name}:{script_name} runs {match.group(1)}, which does not exist")
                continue

            tree = ast.parse(script.read_text(), filename=str(script))
            imported: dict[str, str] = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("dependency"):
                    for alias in node.names:
                        imported[alias.asname or alias.name] = f"{node.module}.{alias.name}"

            for node in ast.walk(tree):
                if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
                    continue
                dotted = imported.get(node.func.id)
                if dotted is None:
                    continue
                module_name, _, attribute = dotted.rpartition(".")
                try:
                    target = getattr(importlib.import_module(module_name), attribute)
                    signature = inspect.signature(target)
                    signature.bind(*[None] * len(node.args), **{k.arg: None for k in node.keywords if k.arg})
                except TypeError as exc:
                    report.fail(
                        "hatch_scripts",
                        f"{match.group(1)}:{node.lineno} calls {node.func.id}(): {exc}",
                    )
                except Exception as exc:  # pragma: no cover
                    report.advise("hatch_scripts", f"cannot check {dotted}: {exc}")


# ------------------------------------------------------------ package markers

def check_package_markers(report: Report) -> None:
    """Every directory holding modules must be a regular package, not a namespace one.

    An implicit namespace package can be shadowed by any other distribution that installs
    the same path, and mkdocstrings cannot collect from one -- `core/utils` went
    undocumented for that reason until it was found by the docs build.
    Rule: docs/architecture.md, "Where a new file goes".
    """
    example = ROOT / "src" / "example"
    directories = {p.parent for p in source_files()}
    directories |= {p.parent for p in example.rglob("*.py") if "__pycache__" not in p.parts}
    for directory in sorted(directories):
        if not (directory / "__init__.py").exists():
            report.fail(
                "package_markers",
                f"{directory.relative_to(ROOT)} holds modules but has no __init__.py "
                f"(implicit namespace package)",
            )


# --------------------------------------------------- library stays undeclared

FRAMEWORK_DECORATORS = {"component", "instance", "product", "module"}


def check_library_undecorated(report: Report) -> None:
    """Nothing in library/ may carry a framework decorator.

    Declaration is a global import-time side effect and `Injectable.set_implementation`
    is last-wins, so a component declared by a library would make the active
    implementation depend on import order rather than on intent -- measured, see D-030.
    library/ ships undecorated `Component` contracts and implementation mixins; the
    application applies the decorators.
    Rule: src/dependency/library/CLAUDE.md.
    """
    library = SRC / "library"
    for path in sorted(library.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                continue
            for decorator in node.decorator_list:
                target = decorator.func if isinstance(decorator, ast.Call) else decorator
                name = target.id if isinstance(target, ast.Name) else None
                if name in FRAMEWORK_DECORATORS:
                    report.fail(
                        "library_undecorated",
                        f"{path.relative_to(ROOT)}:{node.lineno} applies @{name} to "
                        f"{node.name!r}. library/ must not declare providers -- ship an "
                        f"undecorated Component contract and let the application declare it.",
                    )


# --------------------------------------------------------- layering (advisory)

LAYER_ALLOWED = {
    "core.declaration": {"core.agrupation", "core.injection", "core.exceptions"},
    "core.agrupation": {"core.injection", "core.resolution", "core.exceptions", "core.utils"},
    "core.injection": {"core.resolution", "core.exceptions"},
    "core.resolution": {"core.injection", "core.utils", "core.exceptions"},
    "core.utils": set(),
    # library depends on core, never the other way round (D-019, now one-directional)
    "library": {"core", "core.injection", "core.utils"},
    "cli": set(),
    "core": {"core.agrupation", "core.declaration", "core.injection", "core.resolution", "core.exceptions"},
}
KNOWN_CYCLES = {("core.injection", "core.resolution")}


def _layer(dotted: str) -> str:
    parts = dotted.split(".")
    if len(parts) >= 3 and parts[1] == "core":
        return f"core.{parts[2]}"
    return parts[1] if len(parts) >= 2 else dotted


def check_layering(report: Report) -> None:
    """Report the dependency direction between core subpackages and library.

    ADVISORY: one cycle is accepted, core.injection <-> core.resolution (D-018). A second
    is not -- it is reported as a failure. The core -> library cycle is closed (D-019).
    Rule: src/dependency/core/CLAUDE.md.
    """
    edges: set[tuple[str, str]] = set()
    for path in source_files():
        source_layer = _layer(".".join(path.relative_to(SRC.parent).with_suffix("").parts))
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            target = None
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("dependency."):
                target = _layer(node.module)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("dependency."):
                        target = _layer(alias.name)
            if target and target != source_layer:
                edges.add((source_layer, target))

    cycles = {tuple(sorted(pair)) for pair in edges if (pair[1], pair[0]) in edges}
    for cycle in sorted(cycles):
        if cycle in KNOWN_CYCLES or tuple(reversed(cycle)) in KNOWN_CYCLES:
            report.advise("layering", f"accepted cycle {cycle[0]} <-> {cycle[1]} (D-018)")
        else:
            report.fail("layering", f"new dependency cycle {cycle[0]} <-> {cycle[1]}")

    for source_layer, target in sorted(edges):
        allowed = LAYER_ALLOWED.get(source_layer)
        if allowed is not None and target not in allowed:
            report.advise("layering", f"undeclared edge {source_layer} -> {target}")


# --------------------------------------------------- name collisions (advisory)

def check_name_collisions(report: Report) -> None:
    """Two providers with the same class name under one container overwrite silently.

    ADVISORY for tests, where each test owns its Container and collisions are harmless.
    Rule: tests/CLAUDE.md, src/dependency/core/CLAUDE.md. See D-020.
    """
    seen: dict[str, list[str]] = {}
    for path in sorted((ROOT / "tests").rglob("*.py")):
        for node in ast.parse(path.read_text(), filename=str(path)).body:
            if isinstance(node, ast.ClassDef):
                seen.setdefault(node.name, []).append(str(path.relative_to(ROOT)))
    duplicates = {name: files for name, files in seen.items() if len(files) > 1}
    if duplicates:
        total = sum(len(files) - 1 for files in duplicates.values())
        report.advise(
            "name_collisions",
            f"{total} duplicate declared class names across test files "
            f"(worst: {max(duplicates, key=lambda n: len(duplicates[n]))} in "
            f"{max(len(f) for f in duplicates.values())} files). Harmless while each test "
            f"builds its own Container.",
        )


# ------------------------------------------------------------- api snapshot

def check_api_snapshot(report: Report) -> None:
    """The public API only changes with the version number.

    Rule: CLAUDE.md, "Packaging and compatibility". Backward compatibility is a
    constraint of this project, and nothing else enforces it.
    """
    try:
        import dependency.core as core
    except ImportError as exc:  # pragma: no cover
        report.advise("api_snapshot", f"cannot import dependency.core: {exc}")
        return

    current = sorted(core.__all__)
    missing_exports = [name for name in current if not hasattr(core, name)]
    for name in missing_exports:
        report.fail("api_snapshot", f"__all__ lists {name!r} but dependency.core has no such attribute")

    if not SNAPSHOT.exists():
        SNAPSHOT.write_text(json.dumps({"version": pyproject()["project"]["version"], "core": current}, indent=2) + "\n")
        report.advise("api_snapshot", f"created {SNAPSHOT.relative_to(ROOT)} with {len(current)} names")
        return

    recorded = json.loads(SNAPSHOT.read_text())
    removed = sorted(set(recorded["core"]) - set(current))
    added = sorted(set(current) - set(recorded["core"]))

    def major(version: str) -> int:
        return int(version.split(".")[0])

    this_version = pyproject()["project"]["version"]
    if removed and major(this_version) <= major(recorded["version"]):
        report.fail(
            "api_snapshot",
            f"removed from dependency.core.__all__ since {recorded['version']}: "
            f"{', '.join(removed)}. Removing a public name is a breaking change, but the "
            f"version is still {this_version}. Bump the major version and update "
            f"tools/api_snapshot.json in the same commit.",
        )
    elif removed:
        report.advise(
            "api_snapshot",
            f"{len(removed)} name(s) removed since {recorded['version']}, covered by the "
            f"major bump to {this_version}: {', '.join(removed)}",
        )
    if added:
        report.advise("api_snapshot", f"new public names since {recorded['version']}: {', '.join(added)}")


CHECKS = [
    check_version_floor,
    check_forward_refs,
    check_declared_imports,
    check_stub_parity,
    check_docs_references,
    check_document_map,
    check_cli_templates,
    check_changelog_version,
    check_hatch_scripts,
    check_package_markers,
    check_library_undecorated,
    check_layering,
    check_name_collisions,
    check_api_snapshot,
]


def main() -> int:
    report = Report()
    for check in CHECKS:
        report.checks_run += 1
        check(report)

    if report.advisories:
        print(f"\n  ADVISORIES ({len(report.advisories)}) — these stop nothing\n")
        for line in report.advisories:
            print(f"    · {line}")

    if report.failures:
        print(f"\n  FAILURES ({len(report.failures)})\n")
        for line in report.failures:
            print(f"    ✗ {line}")
        print(f"\n  {len(report.failures)} failure(s) across {report.checks_run} checks.\n")
        return 1

    print(f"\n  {report.checks_run} checks passed, {len(report.advisories)} advisories.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
