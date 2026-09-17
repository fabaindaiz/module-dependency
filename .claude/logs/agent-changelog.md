# Agent changelog

One entry per change with an architectural consequence, **newest first**.

This file exists because parallel sessions cannot see each other. Two sessions worked this
repo's resolution refactor without knowing: `registry.py` and `fallback.py` were deleted
while `docs/ARCHITECTURE.md`, `docs/reference/core.md` and two docstrings kept describing
them. The docs build had been failing since, and nobody found out because it only runs on
release.

`CHANGELOG.md` is different: it is user-facing, one entry per **released version**.

Format:

```markdown
## YYYY-MM-DD — <one-line title>
**What.** What changed, concretely.
**Areas.** Files or folders.
**Why.** The reason, including the request that prompted it.
**Architecture.** ✅ Complies · ⚠️ Deviation · REVIEW — and why.
**Measured.** The number, if a claim was made.
```

---

## 2026-09-17 — The example is an application now, not a catalogue of patterns

**What.** Replaced `src/example` with a working monitoring station, and finished the two
library items that needed no further decision.

*Library.* `CompositeComponent`/`CompositeMixin` and `StateComponent`/`StateMixin`, joining
the observer pair. `Composite.getChildren()` became the `children` property.
`library/` went from 23% to 94% coverage over 32 new tests; `graph/`, which had none, is at
96–100%. Removed the `if __name__ == '__main__'` demo blocks.

*The example.* Five plugins — `runtime` (clock, async loop, station state), `sensors`
(probes over a plain ABC, a composite group, a sampler), `storage` (memory or JSONL),
`telemetry` (events, observer, alerts) and `display` (**optional**). Deleted the GoF
catalogue under `module/`. Every framework feature now has one place that demonstrates it,
and `tests/example/` fails if any of it stops working.

**Areas.** `src/dependency/library/`, `src/example/` (rewritten), `tests/library/`,
`tests/example/`, `docs/`, `src/main.py`, `src/graph.py`, `stubs/`.

**Why.** Requested: continue the roadmap, and make the example genuinely an application of
the kind this library targets. The GoF catalogue showed patterns, not what the framework
is for — a reader could not tell from it why they would choose it.

**Architecture.** ✅ Complies. No framework behaviour changed. Two limits were *found*, not
introduced, and are documented rather than worked around silently.

**Measured.**

- **Building the example found two framework limits.** `container.shutdown_resources()`
  and `init_resources()` both do nothing: the root container's `.providers` is
  `['__self__']` because plugin providers live in nested sub-containers it does not track.
  That is the same root cause as D-005, and it explains the unexplained TODO in
  `tests/core/test_resource.py`. D-034.
- **Bootstrap order is unspecified** — `ResolutionStrategy.initialize` iterates a `set`. The
  first draft sampled during `__init__` and published warm-up readings before the alert
  sink had subscribed, intermittently. The warm-up is now sequenced from the entrypoint.
  D-035.
- **`optional=` verified both ways.** With `DisplayPlugin` the panel is wired and mirrors
  alerts; without it the station logs *"no status panel on this unit"* and keeps sampling.
  The headless case runs in a subprocess, because declaration is process-global and the two
  stations cannot coexist in one interpreter.
- Tests: **48 → 87**. `mypy --strict` clean on 48 source files, and `src/example` now has
  one known error left, the `LazyWiring` stub interaction.
- `Sampler.warmup()` exists solely because of D-035. Do not move it back into `__init__`.

**Not done.** The version is still `1.1.7`; `check_api_snapshot` fails deliberately until
that is decided. `LazyWiring` keeps `src/example` out of the gate's typecheck.

## 2026-09-17 — Reusable building blocks: library ships contracts, not declarations

**What.** Answered the open product question from the roadmap — whether "pre-defined
components" ship as declared components or as base classes — and implemented the answer.

- New `dependency.library.components` with `ObserverComponent[CONTEXT]` (an **undecorated**
  `Component` contract) and `EventPublisherMixin[CONTEXT]` (the implementation body).
- Refactored `example/plugin/hardware/observer/` onto them as the worked case. Per-domain
  boilerplate went from ~15 lines to 4.
- New audit check `check_library_undecorated`: no `@component`, `@instance`, `@product` or
  `@module` may appear anywhere under `library/`.
- **Closed the `core → library` cycle.** `handle_exit` moved to `core/utils/threading.py`;
  `library/threading.py` re-exports it, so the old import path still works. `library` now
  depends on `core` and never the reverse. D-019 changed from "accepted debt" to "closed".
- Added the nine missing `__init__.py` files under `src/example`, and extended
  `check_package_markers` to cover it.
- Renamed `validation.standalone_provider(cls=...)` to `provided_cls`, and annotated it as
  `type[T]`.

**Areas.** `src/dependency/library/`, `src/dependency/core/utils/threading.py`,
`src/dependency/core/agrupation/entrypoint.py`,
`src/dependency/core/declaration/validation.py`, `src/example/`, `tools/audit_dependency.py`,
`docs/`, `stubs/`.

**Why.** Requested: implement the decision, considering what could break backward
compatibility — with the note that the project is not yet in heavy use, which is what made
closing the cycle and renaming a parameter acceptable now rather than at a major version.

**Architecture.** ✅ Complies, and improves. One accepted cycle removed; the layering rule is
now `library → core`, one-directional, and a third cycle is a failure rather than an
advisory.

**Backward compatibility.** Nothing in `dependency.core.__all__` changed. `library/components`
is new. `dependency.library.threading.handle_exit` still imports from the same path via a
re-export. The one behavioural change is `validation.standalone_provider` / `validate_provider`
renaming their first parameter, which breaks only a caller passing it by keyword — both
internal call sites are positional, and neither function is in `__all__`.

**Measured.**

- **The decision was made on three measurements, not on taste.** `EventBus.injection` is a
  class attribute — one node per process. A library default plus an application override
  logs `Provider EventBus implementation reassigned: DefaultEventBus -> AppEventBus` on
  every startup. And the last decorator applied wins, so **which implementation runs depends
  on import order**. The alternative was verified too: two domains declaring from the same
  undecorated contract get independent injection nodes
  (`HardwarePlugin.HardwareObserver` and `ReporterPlugin.ReporterObserver`), with no
  reassignment warning.
- **`mypy --strict src/example`: 28 errors → 1.** The example had never been type-checked at
  all — mypy refused to map its modules because nine directories had no `__init__.py`.
  The remaining error is `LazyWiring(_Marker)` reporting unimplemented abstract attributes
  when the stub is checked standalone.
- **`stubgen` strips the annotation from any parameter named `cls`**, treating it as a
  classmethod's implicit first argument. `validation.standalone_provider(cls: type[T], ...)`
  had been shipping to consumers as `(cls, ...)` — untyped — for the life of the project.
  Renaming to `provided_cls` fixed it; reformatting the signature did not. D-032.
- Contracts must be `Generic` in their domain type or `mypy --strict` rejects every
  domain-typed override as a Liskov violation. Verified both ways. D-031.
- Gate after the change: 48 tests, `mypy --strict` clean on 46 source files, 14 audit checks
  with 1 deliberate failure and 3 advisories — one fewer advisory than before, because the
  `core → library` cycle is gone.

## 2026-09-17 — Bootstrap the agent instruction system, and fix the nine violations it found

**What.**

*The instruction system.* Root `CLAUDE.md` (157 lines, budget 200); five area files
(`src/dependency/core/`, `cli/`, `library/`, `src/example/`, `tests/`); five skills
(`verify`, `release`, `troubleshoot-resolution`, `workflow`, `state-review`);
`.claude/settings.json` with `permissions.deny` on the generated `stubs/`;
`docs/decisions.md` (29 rows), `docs/references.md` (14 annotated sources),
`docs/roadmap.md`, `.editorconfig`, and `tools/audit_dependency.py` — **13 structural
checks** wired into a new `hatch run build:gate` (`tests` → `typecheck` → `audit`).

*Product bugs the audit found, all fixed.*

- `requires-python` `>=3.11` → `>=3.12`; `.mypy.ini` `python_version` 3.13 → 3.12; CI
  3.13 → 3.12. `typing.override` is 3.12+ so the package could never import on 3.11.
- `library/graph/models.py` reordered bottom-up. It had **two** unquoted forward
  references, `Drawable` and `Edge` — the second one I had missed by hand and the check
  found.
- `graphviz` declared as the `[graph]` extra, with an import guard that names the extra
  instead of raising a bare `ModuleNotFoundError`.
- `dependency_injector` bounded to `>=4.48.2,<5` — the release that introduced
  `warn_unresolved`, which `ResolutionStrategy.wiring` depends on.
- `src/graph.py` now passes `PLUGINS` to `generate_graph()`.
- All four `cli/templates/*.j2` rewritten against the live decorator signatures.
  `plugin.py.j2` also generated a `config()` **method** where the framework reads a
  `config:` **type hint** — a third defect the decorator-keyword check did not cover.
- The two `mypy --strict` errors in `library/graph/`.
- Added the missing `__init__.py` to `core/utils/` and `library/`. They were implicit
  namespace packages, which is why `utils` could never be documented.

*Documentation corrected against the code.*

- `docs/ARCHITECTURE.md` → `docs/architecture.md`, rewritten. Deleted the `Registry`,
  `Fallback Plugin` and `partial_resolution` sections — none of those exist — and replaced
  the "five sequential phases" description with the actual four-step `ProviderExpansion`.
- `docs/reference/core.md` no longer points at the deleted `resolution.registry`; added
  `resolution.expansion` and `utils.cycle`.
- Fixed the two docstrings that still claimed `partial_resolution` exists
  (`expansion.py::_cascade_failures`, `injection.py::ProviderInjection`).
- `docs/README.md` deleted. The root `README.md` is canonical (PyPI reads it) and
  `docs/index.md` replaces the duplicate, which had already drifted in three places.
- Fixed `README.md`, which taught `from dependency.core.injection import LazyProvide,
  inject` — `inject` is not exported there. Added the Python requirement and the extra.
- Renamed docs to lowercase via `git mv`. macOS is case-insensitive and CI runs on Linux;
  writing `docs/references.md` silently overwrote `docs/REFERENCES.md` in place.
- Dead `[tool.mypy]` block deleted from `pyproject.toml`; `.mypy.ini` always won.
- `CHANGELOG.md`: added the missing v1.1.6 and v1.1.7 entries with their real tag dates,
  plus an `[Unreleased]` section flagging the breaking API change.
- `mkdocs.yaml`: new `Project` nav section, `exclude_docs` for `docs/agents/`, and the
  placeholder `repo_url` (`github.com/tu-usuario/...`) corrected.

*CI.* `testing.yml` runs the gate instead of only tests. `release.yml` runs the gate and
then installs the built wheel into a clean venv and imports every public module, before
publishing.

**Areas.** `CLAUDE.md`, `.claude/`, `docs/`, `tools/`, `pyproject.toml`, `.mypy.ini`,
`.editorconfig`, `.github/workflows/`, `README.md`, `CHANGELOG.md`, `mkdocs.yaml`,
`src/graph.py`, `src/dependency/library/`, `src/dependency/cli/templates/`,
`src/dependency/core/{injection,resolution}/`, `stubs/`.

**Why.** Requested: prepare this repository to be worked on with Claude Code, following
`docs/agents/bootstrap-prompt.md`. The user added one constraint — preserve backward
compatibility, with Python 3.12 as the floor.

**Architecture.** ✅ Complies. No framework behaviour changed. Two semantic changes, both
additive: `library/graph` now raises a message naming the `[graph]` extra rather than a
bare `ModuleNotFoundError`, and `core/utils` / `library` became regular packages.

**Measured.**

- The audit failed **12 of 12 checks on its first run** — 9 real product bugs plus 3
  not-yet-written documents. It now reports **1 failure across 13 checks**, and that one is
  deliberate (see REVIEW below).
- `mypy --strict`: **2 errors → 0**, across 43 source files.
- `hatch run docs:build`: **`BuildError` → builds in 0.88s**. It had been failing on
  `dependency.core.resolution.registry` since the refactor, and only runs on release.
- `hatch run build:graph`: **`TypeError` → renders an 8866-byte SVG**.
- Clean-venv wheel installs, measured on four interpreters: **3.11 → `ImportError:
  cannot import name 'override'`**; **3.12 and 3.13 → `NameError: name 'Drawable' is not
  defined`**; **3.14 → clean**. After the fixes, all 12 public modules import on 3.12 and a
  declare→resolve→provide round trip passes from the installed wheel.
- **Coverage was 91% and is now 78%, and the 78% is the true figure.** Adding the two
  missing `__init__.py` files made **127 previously-undiscovered statements** visible —
  all of `library/graph/` plus `patterns/composite.py` and `patterns/state.py`. Nothing
  regressed; the 91% had never been true. D-029.
- `--dist=loadfile` is **not** test isolation: the suite passes serially in a single
  process (48 tests, **0.18s**), with `-n 1`, and with `--dist=load`. The real boundary is
  one `Container` per test. D-023.
- `container.check_dependencies()` validates nothing here: **0** `providers.Dependency` in
  the entire example-app container tree, because `validation._PROVIDERS` makes them
  impossible to construct. D-005.
- `[tool.mypy]` in `pyproject.toml` never applied — `mypy -v` prints
  `Config File: .mypy.ini`. D-024.
- Two same-named plugins produce the identical reference `TPlugin.TService` and the second
  **silently overwrites** the first. **27** duplicate class names exist across test files
  today; harmless only because each test owns its `Container`. D-020.
- Self-consistency check: 13 checks defined, 13 registered, 13 cited by a written rule;
  29 decisions defined, 29 cited. No rule names a check that does not exist.

**REVIEW — needs a human decision.** `Registry` left `dependency.core.__all__` in the
unreleased refactor while the version is still `1.1.7`, the version that contained it.
Under semantic versioning the next release is `2.0.0`. `check_api_snapshot` fails until
that is decided, and the failure is intentional: it is the backward-compatibility enforcer
doing its job on its first real case. Fixing it is two lines — the version in
`pyproject.toml` and `tools/api_snapshot.json`.

**Not done, deliberately.** No version bump (a release decision). The pydantic mypy plugin
is not enabled — the dead config block was deleted but turning the plugin on may surface
type errors that now block the gate, so it is a roadmap item. No formatter or linter
adopted (D-025). `testing.py` at the repo root left untouched, assumed to be a design
spike, recorded as an open question.
