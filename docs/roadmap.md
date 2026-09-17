# Planned work

Accepted ideas, not yet built. **Not a promise and not a work order:** this is where each
one will collide, written now while it is clear.

Decision numbers refer to `decisions.md`.

---

## Where we are

The resolution refactor (`cdf761c`, unreleased) replaced the global `Registry` and the
`FallbackPlugin` with `ProviderExpansion` — a four-step BFS that discovers undeclared
providers, adopts orphans into their importer's container, and cascades required-import
failures. It is complete and tested: 48 tests, **95% coverage on `core/`**.

It is **unreleased and breaking**: `Registry` left `dependency.core.__all__` and
`ExpansionFailure`/`ExpansionResult` entered. The version is still `1.1.7`, which is the
version that *contained* `Registry`. `audit_dependency.py::check_api_snapshot` fails on
this until the version is bumped — deliberately.

**The immediate open question is the version number for the next release.** Under semver it
is `2.0.0`. Nothing else blocks it.

`library/` is the opposite: **23%**, with `graph/` at 0 — the overall figure is 78%, not
the 91% previously reported, which was inflated because two missing `__init__.py` files
hid 127 statements from coverage entirely (D-029).

Nine bugs found by the bootstrap audit are fixed: the Python floor (3.11 → 3.12), two
unquoted forward references in `library/graph/models.py`, the undeclared `graphviz`
dependency, `src/graph.py` calling `generate_graph()` with no arguments, three broken CLI
templates, two `mypy --strict` errors, and the two missing package markers.

---

## Product direction

The three features the README commits to, with what each one collides with. These are the
project's stated goals; everything below this section is maintenance that serves them.

### 1. Pre-defined components — **decided, and started**

**The decision (D-030).** `library/` ships **undecorated** `Component` contracts plus
implementation mixins; the application applies `@component` and `@instance` itself. It was
measured, not argued: `injection` is a class attribute with one instance per process, a
library default plus an application override logs `implementation reassigned` on every
startup, and **the last decorator applied wins — so which implementation runs depends on
import order, not on intent.**

**What exists.** `library/components/observer.py` with `ObserverComponent[CONTEXT]` and
`EventPublisherMixin[CONTEXT]`, and `plugin/hardware/observer/` refactored onto them as the
worked case: 15 lines of per-domain boilerplate became 4.

**What is left.** Nothing structural. `ObserverComponent`, `CompositeComponent` and
`StateComponent` all ship, each with its mixin, each covered by tests that assert the
contract carries no declaration of its own.

**What to watch.** Contracts must be `Generic` in their domain type (D-031) or every
domain-typed override becomes a `mypy --strict` error. And nothing in `library/` may carry a
framework decorator; `check_library_undecorated` enforces it.

**What would reopen D-030.** If `Injectable.set_implementation` gained explicit override
semantics — something like `@instance(overrides=LibraryDefault)` instead of last-wins —
shipping defaults from the library would become safe and the trade-off would change. That is
a change in the core, not in `library/`.

### 2. Dependency CLI

**Where it actually is.** Four generators and four templates exist and are tested. There is
**no `[project.scripts]` entry**, so there is no installable command — the CLI is a library
nobody can invoke. Its templates emitted keywords no decorator accepted until this pass.

**What it collides with.** D-022 (frozen but usable) and D-013. Adding
`[project.scripts] dependency = "..."` makes the command-line surface public API: flag
names and output layout become things you cannot change without a major version.

**What is already in its favour.** `check_cli_templates` now verifies generated code
against the live decorator signatures with `inspect.signature`, so the generators cannot
silently rot again. The models (`cli/models/base.py`) already describe the inputs a
command would parse.

**What must be decided first.** What the command actually does. "Generate a plugin
skeleton" and "inspect the resolved graph of an installed app" are both defensible and
share no code. Also: which argument parser, since that becomes a dependency.

### 3. Pytest integration

Covered under **Testing** below — it is the same item as the first-party plugin, and the
measurement in D-023 is what makes it tractable.

### 4. Migration guide — the one the README has owed the longest

The README lists this under "pending issues that eventually will be addressed", and it is
now the most urgent item in this document: the unreleased refactor removed `Registry` and
the fallback plugin, which is a `2.0.0`.

**What it collides with.** Nothing technical. It collides with the fact that `CHANGELOG.md`
stopped at v1.1.5 while two releases shipped (D-026), so the raw material for the guide was
never written down and has to be reconstructed from the diff.

**What is already in its favour.** `tools/api_snapshot.json` records the exact public API of
v1.1.7, so the removed and added names are now a mechanical diff rather than an archaeology
exercise. `docs/decisions.md` explains *why* each thing changed, which is the half a
changelog usually lacks.

**What must be decided first.** Whether `Registry` gets a deprecation shim in a `1.2.0` that
warns, or whether `2.0.0` removes it outright. A shim is friendlier and costs a release.

---

## Claims in the README that measurement contradicts

The README lists these under "recently added". They are not finished, and the roadmap should
say so rather than inherit the claim:

| README claim | Measured state |
|---|---|
| "Visualization tools for dependency graphs" | Shipped **broken**: `NameError` on 3.12 and 3.13, `graphviz` undeclared, `build:graph` raised `TypeError`, and **zero tests** imported it. All fixed in this pass, still untested |
| "Framework API and extension points for customization" | The hooks exist — `on_declaration`, `on_resolution`, `ResolutionStrategy`, `ResolutionConfig` — but are documented nowhere as an extension story. An extension point nobody can find is not one |
| "Enhance documentation and examples" | `docs/` described `Registry`, `FallbackPlugin` and `partial_resolution`, none of which exist, and the docs build had been failing since the refactor |

Not a criticism of the plan — a correction of the starting position, so the next estimate
is made from where the code is.

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

### Tests for `library/` — **done**

`library/` went from 23% to **94%**; `graph/`, which had no test at all, is at 96–100%.
32 new tests. The render test needs the graphviz `dot` binary, which `pip install graphviz`
does not provide, so it skips itself when absent — and CI now installs it so that it
actually runs there rather than skipping silently.

Remaining gap: `threading.py` at 63%. `excluded` and `threaded` are untested, and both are
concurrency helpers whose failure modes only show under contention.

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

### Put `src/example` in the gate

Adding the nine missing `__init__.py` files let mypy see the example for the first time and
found **28 errors**; 27 are fixed. The example is the teaching artefact, so it should not be
able to rot again.

**What it collides with.** One remaining error: `LazyWiring(_Marker)` reports unimplemented
abstract attributes when the stub is type-checked standalone. It is an interaction between
`stubgen` and `dependency-injector`'s own types, on a class that is not public API, and
`stubs/` cannot be hand-edited (D-015).

**What must be decided first.** Whether to declare `LazyWiring` abstract in the source so
stubgen says so, or to accept a narrowly scoped ignore. Both need checking against what
`stubgen` actually emits.

---

### Let the root container see plugin providers

D-034. `container.shutdown_resources()` and `init_resources()` both silently do nothing
because plugin providers live in sub-containers the root does not track — its `.providers`
is `['__self__']`. `ResolutionConfig.init_container` therefore gates two calls that are
both no-ops, and every application has to shut its own resources down by hand.

**What it collides with.** D-005 records `check_dependencies()` as a no-op for a different
reason; this is the same root cause and would close both. `tests/core/test_resource.py`
already carries a TODO saying `shutdown_resources()` "no está funcionando correctamente" —
it has been known and unexplained for a while.

**What is already in its favour.** `MonitoringStation.stop()` in the example shows exactly
what the framework should be doing: walk `collect_providers()` and shut down each
`di.Resource`. It is a dozen lines.

**What must be decided first.** Whether to register sub-containers with the root so
dependency-injector's own machinery works, or to keep the tree ours and do the walk in
`ResolutionStrategy`. The first is tidier and risks surprising interactions with wiring.

### Make bootstrap order deterministic

D-035. `ResolutionStrategy.initialize` iterates a `set`, so which `bootstrap=True`
component runs first is unspecified. The example works around it by sequencing the
sampler's warm-up from the entrypoint.

**What it collides with.** Nothing, but it is a behaviour change: today's order is
arbitrary, and code may accidentally depend on the arbitrary order it happens to get.

**What is already in its favour.** The resolution layers already compute a valid
topological order in `ResolutionStrategy.injection` — it is discarded rather than reused.

**What must be decided first.** Whether bootstrap follows dependency order (a provider's
imports bootstrap before it, which is what most people would assume) or declaration order.
Dependency order is the useful one and is already computed.

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
| Pre-defined components **as declared components** | **Yes, potentially.** Shipping decorated components puts library code inside the resolution graph. A pre-defined component with a missing optional dependency would now be a startup concern for every consumer |
| Pre-defined components **as base classes** | **No.** They stay outside the graph; the application decorates them |
| Dependency CLI | **No.** It generates source and inspects; it never participates in a running graph |
| Migration guide | **No.** Prose |
| Contract test against `_Marker` | **No.** It protects the wiring the invariant depends on |
| `py.typed` versus stubs | **No.** Type surface only, no runtime effect |
| pytest plugin | **No — the reverse.** It would make the invariant testable in isolation rather than only via the example app |
| Tests for `library/` | **No.** `library/` is outside the resolution path entirely |
| Unrepresentable `reference` collision | **No — the reverse.** It moves a silent overwrite into the class of things that cannot be expressed, which is where D-004 already put invalid providers |
| Break the `injection ↔ resolution` cycle | **No**, but it changes a public hook signature, so it is gated on the major version |
| `ruff` | **No.** Cosmetic |
| pydantic mypy plugin | **No**, but it may block the gate until a backlog of type errors is cleared |

---

## Suggested order

Not a schedule. An order, with the reason each step unblocks the next.

**First — settle the version.** Everything downstream depends on it. `Registry` is gone from
the public API and the version still says `1.1.7`; the audit fails until this is decided.
Pick `2.0.0` (clean) or a `1.2.0` with a deprecation shim (friendlier, costs a release).
Two lines once decided. Blocks: the migration guide, the CLI entry point, pre-defined
components — every item that adds or removes public API.

**Second — write the migration guide and release.** The README has owed it the longest, and
`tools/api_snapshot.json` now makes the API diff mechanical. Releasing also clears
`[Unreleased]` in `CHANGELOG.md` and turns the four bug fixes into something users get.

**Third — pick one product feature, not three.** The three README features have very
different shapes:

| Feature | Blocked on a decision? | Size | Risk to the invariant |
|---|---|---|---|
| Pytest integration | No — D-023 measured the ground | Medium | None; it makes the invariant testable |
| Pre-defined components | **Yes** — declared components or base classes? | Large | Real, if declared |
| Dependency CLI | **Yes** — what does the command do? | Medium | None |

**Pytest integration is the one to do first**, for three reasons: it needs no decision you
have not already made, it is the one whose groundwork exists (the suite is proven to pass in
a single process, so a fixture that resets state has a known-good baseline), and it is the
prerequisite for testing the other two honestly. `library/` sits at 0–55% coverage and
`graph/` has no tests at all; a test story makes that fixable rather than aspirational.

**Fourth — the two contract gaps, whenever there is an hour.** The `_Marker` contract test
and tests for `library/`. Neither needs a decision. Both protect things that already broke
once.

**Leave for last:** `ruff`, the pydantic mypy plugin, breaking the `injection ↔ resolution`
cycle. The first two are noise-generating and better done on a quiet day; the third is gated
on the major version anyway.
