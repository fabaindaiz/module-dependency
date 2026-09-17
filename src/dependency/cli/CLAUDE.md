# cli/ — the `dependency` command

**Status: shipped.** `[project.scripts] dependency = "dependency.cli.main:main"`, and
`docs/reference/cli.md` is in the mkdocs nav. The command surface is public API under
D-013: a flag name or an exit code is as breaking to change as a function signature.

## What it is for

Two jobs, and the second is the one only this framework can offer:

- **Scaffold** — `new plugin|module|component|instance`, wrapping the four generators.
- **Answer whether a graph holds, without starting the application** — `check`, `show`,
  `graph`. Expansion and the topological pass run; **wiring and bootstrap never do**, so
  it is safe to point at somebody else's code in CI.

`argparse`, from the standard library. A CLI that adds a dependency to a
dependency-injection library is a poor trade, and this surface does not need more.

## The one rule

**A template may only emit decorator keywords that exist in the live decorator
signature.** A generator that emits code which raises `TypeError` on import is worse
than no generator: it produces a file that looks right and fails at the user's first run.
The templates were once in violation — `component.py.j2` emitted `interface=` and
`instance.py.j2` emitted `component=`, neither of which any decorator accepted. Enforced
in `audit_dependency.py::check_cli_templates`, which reads the real signatures with
`inspect.signature` rather than a hardcoded list, so it keeps working when the decorators
change.

## The rule `check` exists to enforce

**An empty graph expands cleanly and proves nothing.** A component with no implementation
is not an error on its own (D-002), so a `check` that resolved zero providers has verified
nothing at all — it almost always means no registration module was imported. `check`
reports that as a failure and names the cause, because a verification command that exits 0
on an empty run is worse than no command.

## Structure

- `main.py` — the parser and the dispatch. One function per command, each returning an
  exit code; `main()` turns `EntrypointError`, `DependencyError` and `OSError` into a
  one-line message on stderr, never a traceback.
- `inspection.py` — loading a `module:attribute` entrypoint, importing registration
  modules, expanding, and describing the tree.
- `models/base.py` — pydantic input models (`Module`, `Component`, `Instance`).
- `generation/base.py` — the single shared `jinja2.Environment` with a `PackageLoader`.
- `generation/<kind>.py` — one class per template, a single `@staticmethod generate`.
- `templates/<kind>.py.j2` — included in the wheel by hatchling automatically. Verified
  present in the built wheel; no `MANIFEST.in` is needed.

Copy `generation/component.py` for a new generator. It is four lines of substance.

## When changing a decorator in `core/declaration/`

Update the matching template in the same commit. The audit will catch it, but the point
is that these two files are one contract split across two languages.
