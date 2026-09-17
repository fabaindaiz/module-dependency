# cli/ — the code generator

**Status: frozen but intended to stay usable.** No console entry point is declared, and
`docs/reference/cli.md` is not in the mkdocs nav. It ships in the wheel and it is meant
to work.

## The one rule

**A template may only emit decorator keywords that exist in the live decorator
signature.** A generator that emits code which raises `TypeError` on import is worse
than no generator: it produces a file that looks right and fails at the user's first run.

The templates are currently in violation. `component.py.j2` emits `interface=` and
`instance.py.j2` emits `component=`; neither parameter exists in
`dependency.core.declaration`. Enforced in `audit_dependency.py::check_cli_templates`,
which inspects the real signatures with `inspect.signature` rather than a hardcoded list,
so it keeps working when the decorators change.

## Structure

- `models/base.py` — pydantic input models (`Module`, `Component`, `Instance`).
- `generation/base.py` — the single shared `jinja2.Environment` with a `PackageLoader`.
- `generation/<kind>.py` — one class per template, a single `@staticmethod generate`.
- `templates/<kind>.py.j2` — included in the wheel by hatchling automatically. Verified
  present in the built wheel; no `MANIFEST.in` is needed.

Copy `generation/component.py` for a new generator. It is four lines of substance.

## When changing a decorator in `core/declaration/`

Update the matching template in the same commit. The audit will catch it, but the point
is that these two files are one contract split across two languages.
