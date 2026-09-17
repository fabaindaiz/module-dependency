# Planned work

Accepted ideas, not yet built. **Not a promise and not a work order:** this is where each
one will collide, written now while it is clear.

Decision numbers refer to `decisions.md`.

---

## Where we are

The resolution refactor (`cdf761c`, unreleased) replaced the global `Registry` and the
`FallbackPlugin` with `ProviderExpansion` — a four-step BFS that discovers undeclared
providers, adopts orphans into their importer's container, and cascades required-import
failures. It is complete and tested (48 tests, 91% coverage on `core/`).

It is **unreleased and breaking**: `Registry` left `dependency.core.__all__` and
`ExpansionFailure`/`ExpansionResult` entered. The version is still `1.1.7`, which is the
version that *contained* `Registry`. `audit_dependency.py::check_api_snapshot` fails on
this until the version is bumped — deliberately.

**The immediate open question is the version number for the next release.** Under semver it
is `2.0.0`. Nothing else blocks it.

Four bugs found during the bootstrap audit are fixed: the Python floor (3.11 → 3.12),
the unquoted forward references in `library/graph/models.py`, the undeclared `graphviz`
dependency, and `src/graph.py` calling `generate_graph()` with no arguments. The CLI
templates, which generated code that raised `TypeError` on import, are rewritten.

---

## Compatibility and packaging

### Contract test against `dependency-injector`'s private API

`injection/wiring.py` imports `_Marker` — an underscore-prefixed class. An upstream
refactor breaks every installed user, and we would learn about it from an issue report.

**What it collides with.** Nothing. This is the rare item with no trade-off.

**What is already in its favour.** The `<5` upper bound (D-012) buys time but does not
detect anything. The test would be ten lines.

**What must be decided first.** Whether the test asserts *shape* (the names exist, the
constructor takes what we pass) or *behaviour* (a wired injection actually resolves). The
second is stronger and slower.

### Decide `py.typed` versus generated stubs

Today the `.pyi` files are the only type surface consumers see (D-015, PEP 561). Adding
`py.typed` and deleting `stubs/` would be simpler and would remove an entire class of drift.

**What it collides with.** D-015, and the wheel layout — `dependency-stubs/` is force-included
by hatchling. Removing it changes what consumers resolve types from, so it is a
compatibility change, not a cleanup.

**What must be decided first.** Whether any downstream project pins against the stubs.
Unknown.

---

## Testing

### First-party pytest plugin

`dishka` and `modern-di` ship one. Ours would own the thing that is currently convention:
a fresh `Container` per test, and ideally a reset of the process-global declaration state.

**What it collides with.** D-023 — the current isolation boundary is "one `Container` per
test", enforced by nothing but habit. A plugin that resets global state would change that
boundary, and 27 duplicate class names across test files (D-020) become meaningful the
moment two of them share a container.

**What is already in its favour.** The measurement exists: the suite passes serially, so we
know the current state is sound and any regression is attributable.

**What must be decided first.** Is the declaration registry resettable at all? `@component`
mutates class attributes with no teardown path. That question decides whether this is a
fixture or a redesign.

### Tests for `library/`

`patterns/` and `threading.py` sit at 55% coverage; `library/graph/` has **no test at all**
and does not even appear as a row in the coverage report, while the total reads 91%. The
`NameError` that broke `graph` on every supported Python shipped through that gap.

**What it collides with.** Nothing structural. `graph/` needs the `[graph]` extra installed
in the test environment.

**What must be decided first.** Whether `library/` deserves the same coverage bar as `core/`,
given it is explicitly "part of the product but not primordial".

---

## Structure

### Make the `reference` collision unrepresentable

Two providers with the same class name under one container overwrite silently via `setattr`
(D-020, measured). Rung 4 would be a `ContainerInjection.attach` that refuses.

**What it collides with.** It would turn a currently-silent condition into an error, and
tests have 27 duplicate names today. They are in different containers so they should pass —
but "should" is doing work in that sentence.

**What is already in its favour.** `audit_dependency.py::check_name_collisions` reports the
count, so the blast radius is known before the change.

**What must be decided first.** Hard error or warning? A hard error is the honest choice and
the riskier one.

### Break the `injection ↔ resolution` cycle

D-018. `ContainerMixin.on_resolution` takes a `Container`, which is what forces
`injection/mixin.py` to import from `resolution/`.

**What it collides with.** `on_resolution` is a public hook — `example/plugin/base/__init__.py`
overrides it. Changing its signature is a breaking change, so it belongs with the 2.0.0
release or never.

**What must be decided first.** Whether a `Protocol` in `injection/` that `Container`
structurally satisfies is enough, or whether the hook signature has to change.

---

### A plugin without config logs a warning

`Plugin.resolve_container` logs at WARNING level when the `config:` type hint is absent or
is not a `BaseModel`. A plugin that genuinely needs no configuration is a normal case, so
the first thing a new user sees is a warning about nothing.

**What it collides with.** Nothing structural. It is one branch in
`agrupation/plugin.py::resolve_container`.

**What must be decided first.** Whether "no config" and "config of the wrong type" should
stay one message. They are different situations: the second is a real mistake.

---

## Tooling

### Adopt `ruff`

**What it collides with.** D-025 — formatting 2941 LOC buries every meaningful diff. It must
be its own commit, and the commit must contain nothing else.

**What must be decided first.** Format-only, or lint rules too? Lint rules on an unlinted
codebase produce hundreds of findings and someone has to triage them.

### Enable the pydantic mypy plugin

It was configured in `[tool.mypy]` in `pyproject.toml` and **never loaded** — `.mypy.ini`
wins (D-024, verified with `mypy -v`). The dead block is deleted; the intent is not.

**What it collides with.** Nothing structural, but it may surface type errors that have been
hidden for the whole life of the project. `typecheck` is now in the gate, so those errors
become blocking the day the plugin is enabled.

**What must be decided first.** Nothing — just do it on a day when a pile of new mypy errors
is welcome.

---

## Closed by measurement

| Idea | The number that closed it |
|---|---|
| "`--dist=loadfile` protects tests from each other" | The suite passes serially in one process (48 tests, 0.18s), with `-n 1`, and with `--dist=load`. `loadfile` only co-locates a file's tests on one worker; 18 files across 6 workers share interpreters anyway. D-023 |
| "`check_dependencies()` is part of our validation" | 0 `providers.Dependency` in the entire example-app container tree — `validation._PROVIDERS` makes them impossible to construct. D-005 |
| "`[tool.mypy]` in `pyproject.toml` configures our type checking" | `mypy -v` prints `Config File: .mypy.ini`. The block never applied. D-024 |
| "Data files might be missing from the wheel" | Inspected the built wheel: all four `.j2` templates present, and `dependency-stubs/` correctly force-included. Not a problem here, and no `MANIFEST.in` is needed |

---

## What each idea costs the core invariant

*Does it break "the entire dependency graph is validated before the first user object is
constructed"?* (D-001)

| Idea | Breaks it? |
|---|---|
| Contract test against `_Marker` | **No.** It protects the wiring the invariant depends on |
| `py.typed` versus stubs | **No.** Type surface only, no runtime effect |
| pytest plugin | **No — the reverse.** It would make the invariant testable in isolation rather than only via the example app |
| Tests for `library/` | **No.** `library/` is outside the resolution path entirely |
| Unrepresentable `reference` collision | **No — the reverse.** It moves a silent overwrite into the class of things that cannot be expressed, which is where D-004 already put invalid providers |
| Break the `injection ↔ resolution` cycle | **No**, but it changes a public hook signature, so it is gated on the major version |
| `ruff` | **No.** Cosmetic |
| pydantic mypy plugin | **No**, but it may block the gate until a backlog of type errors is cleared |
