---
name: release
description: The pre-ship check for the bugs this repo cannot see from the source tree.
  Use before publishing, when bumping the version, after touching pyproject.toml, after
  adding any import, after changing anything in library/, and whenever asked to "release",
  "publish", "cut a version", or "is this safe to ship".
allowed-tools: Bash, Read
---

# Release check

**The class of bug this repo cannot observe:** anything that only breaks on an interpreter
other than the local one, or in a module no test imports.

The development environment runs a newer Python than CI, and both run newer than the
declared floor. It also has `graphviz`, `uvloop` and `mypy` installed, which the published
wheel does not declare. Four bugs shipped through exactly that gap:

- `typing.override` (3.12+) while `requires-python` claimed `>=3.11` — the package could not
  be imported at all on 3.11.
- Unquoted forward references in `library/graph/models.py` — `NameError` on 3.12 and 3.13,
  fine on 3.14, which is what the dev machine runs.
- `graphviz` imported but never declared — worked from the source tree, failed for every
  user who pip-installed.
- `src/graph.py` calling `generate_graph()` with a required argument missing.
- `dependency.testing` importing `pytest` at module level while `pytest` lives only in the
  `testing` extra — caught by **this check**, at 2.0.0, before it shipped.

None of these were visible from `git status`, and the test suite was green for all four.

## The check

Run every step. Do not skip the clean venv — it is the only step that reproduces a user.

```bash
# 1. The gate must pass first
hatch run build:gate

# 2. Build the wheel
hatch build -t wheel

# 3. Install it into a clean venv on the MINIMUM supported Python, not the newest.
#    Read the floor from requires-python in pyproject.toml.
hatch python install 3.12
PY=$(hatch python find 3.12)
rm -rf /tmp/mdcheck && "$PY" -m venv /tmp/mdcheck
/tmp/mdcheck/bin/pip install -q "dist/module_dependency-<version>-py3-none-any.whl[graph]"

# 4. Import every public module from the installed wheel
/tmp/mdcheck/bin/python -c "
import importlib
for m in ['dependency.core',
          'dependency.cli.main',
          'dependency.cli.inspection',
          'dependency.cli.generation.component',
          'dependency.cli.generation.plugin',
          'dependency.cli.generation.module',
          'dependency.cli.generation.instance',
          'dependency.library.threading',
          'dependency.library.patterns.observer',
          'dependency.library.patterns.composite',
          'dependency.library.patterns.state',
          'dependency.library.graph',
          'dependency.library.graph.generate']:
    importlib.import_module(m); print('OK  ', m)
"

# 4b. Every entry point must resolve **from the installed distribution**. An entry point is
#     metadata no import exercises, so a typo is invisible from the source tree and fails
#     inside whatever tool consumes it. The gate's check_entry_points covers the dev env;
#     this covers the wheel.
/tmp/mdcheck/bin/pip install -q "dist/module_dependency-<version>-py3-none-any.whl[testing]"
/tmp/mdcheck/bin/python -c "
import importlib.metadata as m
for group, name in [('console_scripts', 'dependency'), ('pytest11', 'dependency')]:
    found = [e for e in m.entry_points(group=group) if e.name == name]
    assert found, (group, name)
    found[0].load(); print('OK  ', group, name)
"
/tmp/mdcheck/bin/dependency version

# 4c. Every extra must name itself when it is missing, never raise a bare
#     ModuleNotFoundError. Install the PLAIN wheel in a second venv for this.
/tmp/mdplain/bin/python -c "
for mod, extra in [('dependency.library.graph', 'graph'), ('dependency.testing', 'testing')]:
    try:
        __import__(mod); raise SystemExit(f'{mod} imported without its extra')
    except ModuleNotFoundError as e:
        assert extra in str(e), e
        print('OK  ', mod, 'names', extra)
"

# 5. Round-trip smoke test: declare, resolve, provide — from the INSTALLED package
/tmp/mdcheck/bin/python -c "
from dependency.core import Container, Entrypoint, Plugin, PluginMeta, module, Component, component, instance, providers
@module()
class P(Plugin): meta = PluginMeta(name='p', version='0.0.1')
@component(module=P)
class S(Component):
    def hi(self) -> str: ...
@instance()
class I(S):
    def hi(self) -> str: return 'ok'
class App(Entrypoint):
    def __init__(self):
        super().__init__(Container.from_dict({'config': True}), [P]); super().initialize()
App(); assert S.provide().hi() == 'ok'; print('ROUNDTRIP OK')
"
```

**When a module, an extra or an entry point is added, add it to the lists above in the same
change.** This check is only as good as what it enumerates, and the bug it caught at 2.0.0
— `dependency.testing` importing `pytest` outside its extra — existed because the module
was new and the list was not updated.

## Before tagging

- `CHANGELOG.md` has an entry for the version in `pyproject.toml`. The audit checks this;
  two releases shipped without one.
- If any name left `dependency.core.__all__`, the major version must increase and
  `tools/api_snapshot.json` must be updated in the same commit (D-013).
- `hatch run docs:build` passes. It runs with `strict: true` on release and a dead
  `::: reference` aborts the GitHub Pages deploy.

## Reporting

Report each step's real output. If the clean-venv install was skipped, say so — that is the
step that catches the bug class, and a release verified without it is not verified.
