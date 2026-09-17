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
**What went wrong on the way.** What the first attempt got wrong, and what caught it. Omit
only if nothing did.
**What was left undone.** Debt this change created or walked past, named, so the next
session does not rediscover it as a surprise.
**Measured.** The number, if a claim was made.
```

**The last three fields are the ones that pay for the file.** A log of successes is
bookkeeping. A log that says *"the first cut cascaded optional failures and only the example
app showed it"*, or *"this file is one function from its line budget and splitting it is a
structural call I did not make"*, is the only mechanism by which one session warns another.
Write the failures in the same voice as the successes: an entry that hides a wrong turn
sends the next session down it.

Earlier entries predate these two fields and are not rewritten.

---

## 2026-09-17 — Bootstrap order becomes a contract, and a plugin without config stops apologising

**What.** `ResolutionStrategy.injection` now returns the order it resolved in, and
`resolution` hands that to `initialize` (D-053, superseding D-035).
`Plugin.resolve_container` separates "no `config:` hint" from "a hint that is not a
`BaseModel`" (D-054). Two roadmap entries closed.

**Areas.** `src/dependency/core/resolution/strategy.py`,
`src/dependency/core/agrupation/plugin.py`, `tests/core/test_resolution.py`,
`tests/core/test_agrupation.py`, `docs/decisions.md`, `docs/roadmap.md`, `stubs/`.

**Why.** Neither needed a decision that was not already implied. `injection` was **already
computing** a valid topological order, layer by layer, and throwing it away — the roadmap
entry said so, and the fix was to stop discarding it rather than to build anything. And a
plugin that needs no configuration is the ordinary case, so the first thing a new user saw
was a warning about nothing.

**Architecture.** ✅ Complies. `injection` gained a return value, which is additive for any
caller that ignored it. Passing a `set` to `initialize` still restores the old unspecified
order, so nothing is forced.

**What went wrong on the way.** The order test passed for the wrong reason on the first
attempt: it asserted on the `BOOTSTRAPED` list another test in the same file fills, which
would have made it depend on test execution order — the exact trap `tests/CLAUDE.md`
already records for `tests/library/test_components.py`. Rewritten as a self-contained
scenario that resolves its own plugin. Also, `ResolutionStrategy` had to be re-imported in
that file: `ruff --fix` had removed it as unused earlier in the session, correctly at the
time.

**What was left undone.** `MonitoringStation.__init__` still sequences the sampler's
warm-up by hand, which existed as the workaround for exactly this. It may now be
unnecessary; that is a checkable follow-up in the example, recorded in the roadmap.

**Measured.** 152 tests + 1 xfailed (was 148), 18 audit checks, 2 advisories, gate green.
The change is visible in the example's own output: `Injectable PressureSensor
initialization skipped` now prints **before** `probe PressureSensor not fitted`, where it
used to print after — the same graph, now in dependency order. Boot: 0.0104 s, zero
warnings.

---

## 2026-09-17 — The CLI becomes a command, and it can answer the invariant from a shell

**What.** `dependency`, declared in `[project.scripts]`, on `argparse` (D-050).
`cli/main.py` and `cli/inspection.py` are new; `tests/cli/test_command.py` covers the
surface and `tests/cli/test_generation.py` was rewritten to actually assert. D-050 to
D-052. The roadmap entry is closed, and `docs/roadmap.md` §Where we are is no longer
claiming the version is unsettled.

**Areas.** `src/dependency/cli/`, `tests/cli/`, `pyproject.toml`,
`tools/audit_dependency.py`, `src/dependency/cli/CLAUDE.md`, `tests/CLAUDE.md`,
`docs/decisions.md`, `docs/roadmap.md`, `stubs/`.

**Why.** The generators existed, were tested and shipped in the wheel, and **nothing could
invoke them** — no console entry point was declared. Beyond scaffolding, the framework has
one thing to say that no general-purpose tool can: *does this dependency graph hold?* That
answer belonged in a shell.

**Architecture.** ✅ Complies. `check` runs expansion and the topological pass and **never**
wiring or bootstrap (D-051), so it is safe to point at somebody else's application in CI:
wiring patches modules, bootstrap runs user code, and a verification command may do
neither. `LAYER_ALLOWED["cli"]` was `set()` — correct when the CLI was a pure generator,
wrong the moment it consumed `core` — and is now declared. Nothing imports `cli`, so no
cycle.

**What went wrong on the way.** Three things, all caught by running the thing rather than
reading it.

A missing config file came out as a **traceback** instead of a message. `main()` now turns
`OSError` and `JSONDecodeError` into one line on stderr.

`check` reported *"0 provider(s) resolved"* and **exited 0** when no registration module had
been imported. That is the worst failure a verification command can have: it certifies a
build in which no `@instance` ever ran. A component with no implementation is not an error
on its own (D-002), so the empty graph expands cleanly and proves nothing. Now it fails and
names the cause (D-052).

And the test for that failure passed alone and failed in the suite, because an earlier test
had already imported the registrations — **declaration is process-global with no teardown**,
so the assertion is only true in a clean interpreter. It runs in a subprocess, following the
precedent `tests/example/test_station_headless.py` already set for the same reason. That is
the fourth time this session that the global declaration state has changed what a test
means.

**What was left undone.** No `--json` output, so the commands are for humans and exit codes,
not for another program to parse. `new` writes one file at a time and lays out no package.
`graph` still needs the graphviz `dot` binary, which `pip install graphviz` does not ship.

**Measured.** 148 tests + 1 xfailed (was 131), gate green on **3.12 and 3.14**, 18 audit
checks, back to 2 advisories. Verified through the installed console script rather than the
module: `dependency version` prints `2.0.0` and `dependency check` on the example resolves
**12 providers across 5 plugins**; with only one registration module imported it prints the
import chains — *"Provider Clock has no implementation (imported via: TemperatureSensor →
Clock)"* — and exits 1.

---

## 2026-09-17 — The formatter enters the gate, and D-025 is superseded on its own terms

**What.** `build:format` (`ruff format --check`, writes nothing) joins the gate, which is
now **tests → typecheck → lint → format → audit → docs**. D-049 recorded; the roadmap's
`Adopt ruff` entry is closed with what the question turned out to be.

**Areas.** `pyproject.toml`, `docs/decisions.md`, `docs/roadmap.md`.

**Why.** D-025 declined the formatter on a number — *"formatting 2941 LOC buries every
meaningful diff"* — and a number is the only thing that should reopen it. Measured: the
diff is **885 lines across 106 files**, and it shipped in a commit containing nothing else,
so nothing was buried.

**Architecture.** ✅ Complies. The gate runs `--check`, never the fixer or the formatter
itself. This repo's own rule is that a formatter does not run on a tree it might be
sharing, and the linter's `--fix` had already proved why in this same session.

**What went wrong on the way.** I claimed in the reformat commit message that `stubgen`
produced byte-identical stubs. **It did not** — four stubs changed. Not signatures, which
were untouched, but docstrings: the formatter collapses `"""Text.\n"""` onto one line
and `stubgen --include-docstrings` carries that through. The commit was local, so the
message was amended to say what actually happened rather than what I expected.

A second suspicion turned out to be unfounded, and is recorded because it was checked: the
formatter moves `# pragma: no cover` from a `raise` onto its closing parenthesis, which
looked like it would silently disable the exclusion. `declaration/validation.py` is still
at 100% with no missing lines — coverage.py honours it there.

**What was left undone.** `mypy` still covers only `src/dependency`; `tests/` and
`src/example/` are unchecked, which is how seven undefined names survived in annotations.
CI runs one interpreter per workflow, so 3.13 is covered locally by `ceiling:gate` and not
in CI. `src/example` is still not in the gate (D-033).

**Measured.** The complete gate — tests, typecheck, lint, format, 18 audit checks and the
docs build — runs in **4.7 s** on 3.14 and **4.6 s** on 3.12, both green. It began this
session as three steps in 3.7 s with one deliberate failure. Coverage after formatting is
unchanged: `core/` 95.0%, total 95.1%.

---

## 2026-09-17 — `ruff` adopted as a linter, and the fixer that deleted the framework's wiring

**What.** `ruff` enters the gate as `build:lint` with a defect-only rule set
(`E4,E7,E9,F,B,BLE`), `imports.py` exempt from `F401`. Twenty-five findings fixed across
`src/`, `tests/` and `tools/`. D-048 recorded. `.ruff_cache` ignored.

**Areas.** `pyproject.toml`, `.gitignore`, `CLAUDE.md`, `docs/decisions.md`, four files in
`src/dependency/`, one in `src/example/`, ten test files, `stubs/`.

**Why.** D-025 declined the **formatter** — *"formatting 2941 LOC buries every meaningful
diff"* — and never ruled on the linter. They are not the same question, and the linter is
the half that finds defects.

**Architecture.** ✅ Complies. `I` and `UP` are deliberately excluded: 119 mechanical
rewrites of imports and annotations, and every annotation change regenerates the stubs,
which are the only type surface a consumer sees (D-015). `SIM` and `C4` reported zero, so
they buy nothing.

**What went wrong on the way.** `ruff check --fix` **deleted every line of all six
`imports.py` files.** Those files exist to import modules for their registration side
effect — the documented mechanism by which an implementation enters a build (D-008) — and
to `F401` they are files of unused imports. The comment explaining why they were there
survived the deletion, sitting above nothing. The example application stopped resolving
with *"Provider Clock has no implementation (imported via: TemperatureSensor → Clock)"*.

The suite caught it in one run, and the attribution was checked rather than assumed: the
tree passed 131 tests before the fix and failed with 8 errors after. Reverted, and the
incident is now a rule — `[tool.ruff.lint.per-file-ignores]` with the measurement written
beside it — rather than a memory. **The gate never runs a fixer**; `build:lint` writes
nothing.

**What the findings were worth.** Not style. Three `B008` on
`strategy: ResolutionStrategy = ResolutionStrategy()` in `entrypoint.py` and `resolver.py`:
one strategy object, built at import, **shared by every caller that omits the argument**,
carrying a mutable `ResolutionConfig`. That is the sixth instance this session of the leak
family the 2.0.0 redesign exists to close, and nothing else in the repository could see it.
Three `B006` mutable defaults in `library/graph/generate.py`. Seven `F821` — annotations
naming `ProviderInjection` in test files that never imported it, invisible because local
annotations are not evaluated and **`mypy` only runs on `src/dependency`**. One `F811`
where `providers` was imported twice and the second silently shadowed the first. Two `B017`
`pytest.raises(Exception)`, and naming the real exception found that `Reading` is a frozen
**dataclass**, not a pydantic model — the broad assertion had been hiding which contract
protects immutability.

**What was left undone.** `mypy` still only covers `src/dependency`; `tests/` and
`src/example/` are unchecked, which is how seven undefined names lived in annotations. The
formatter is next, in a commit containing nothing else.

**Measured.** Gate green on **3.12 and 3.14**: 131 passed + 1 xfailed, `mypy --strict`
clean on 53 files, `ruff` all checks passed, 18 audit checks, 2 advisories. Lint findings
before: 49 across `src tests tools`; after: 0.

---

## 2026-09-17 — The gate gains docs, coverage floors and citation checks — and catches a regression from yesterday

**What.** `build:gate` is now `tests + typecheck + audit + docs`. Three new audit checks —
`check_coverage_floors`, `check_decision_citations` — join yesterday's two, for **18
checks** total. `build:tests` writes `.coverage.json`, which the audit reads. D-044 to
D-047 recorded; `CLAUDE.md` and `docs/roadmap.md` updated.

**Areas.** `pyproject.toml`, `tools/audit_dependency.py`,
`src/dependency/testing/plugin.py`, `CLAUDE.md`, `docs/decisions.md`, `docs/roadmap.md`.

**Why.** To define the gate completely and validate it, rather than assume it.

**Architecture.** ✅ Complies. Every new check is a failure, not an advisory, and each one
was proved to fail on fabricated input before being trusted: a version of 9.9.9, an entry
point that does not resolve, a `D-999` citation, and a floor raised to 99%.

**What went wrong on the way.** The coverage number was **wrong, and I had it backwards**.
Per-package figures read `core/` at 59% against the roadmap's claim of 95%, and I reported
the roadmap as stale. It was not. The cause was
`dependency/testing/plugin.py`, added in this same session: pytest loads entry-point
plugins **before `pytest-cov` starts measuring**, so every module-level import in that
plugin — the whole `dependency.core` chain — executed unmeasured and was then reported as
never run.

| | `core/` | total | `core/__init__.py` |
|---|---|---|---|
| plugin loaded | 59% | 67% | 0% |
| plugin disabled | 95% | 94% | 100% |

A 36-point silent loss on `core/`, introduced hours earlier by a change that had nothing to
do with coverage, and invisible until coverage entered the gate. Fixed by deferring every
framework import into the function that needs it, with the measurement written into the
module docstring so the next session does not tidy them back to the top. D-044.

Also corrected: `docs/roadmap.md` claimed `library/` was at 23% and the total 78%, long
after the library tests landed. Real figures are 99% and 95%. That is the **third** coverage
number in this repository to outlive its measurement, after the 91% D-029 killed and the
59% above — which is the argument for the floors being in a script rather than a sentence.

**What was left undone.** `ruff` is measured but not decided — 922 lines would move under
the formatter and there are 135 lint findings, of which ~110 are syntax modernisation and
about ten are genuine defect signals, including three `B006` mutable-argument-defaults and
one `BLE001` blind-except in a repository whose `CLAUDE.md` calls swallowing exceptions
during bootstrap non-negotiable. CI still runs a single interpreter; 3.13 is covered
locally by `ceiling:gate` and not in CI.

**Measured.** The full gate — tests, typecheck, 18 audit checks and the docs build — runs in
**4.0 s**, up from 3.7 s for the old three-step gate. Green on **3.12 and 3.14**: 131 passed
+ 1 xfailed, `mypy --strict` clean on 53 files, 2 advisories. Coverage after the fix:
`core/` **95%**, `library/` **99%**, `cli/` 100%, total **95%**.

---

## 2026-09-17 — The gate runs on the floor, and now checks the environment it runs in

**What.** Two new hatch environments, `floor` (3.12, the minimum) and `ceiling` (3.13,
which nothing exercised), both templated from `build`. Two new audit checks:
`check_installed_version` and `check_entry_points`. `tests/conftest.py` deleted. Rules
written into `CLAUDE.md` §Commands, §Verification and §Packaging.

**Areas.** `pyproject.toml`, `tools/audit_dependency.py`, `CLAUDE.md`, `tests/conftest.py`.

**Why.** The gate was grading the wrong thing in two different ways, and the first run of
the new environment proved both.

**Architecture.** ✅ Complies. Both checks are failures rather than advisories: neither has
a legitimate exception.

**What went wrong on the way.** This is the entry. The floor environment failed on its
first run with `ValueError: Plugin already registered under a different name:
dependency.testing.plugin`. The cause: `floor` installed the project cleanly, so the
`pytest11` entry point added yesterday actually existed there — and `tests/conftest.py` was
registering the same plugin a second time by hand. **It had worked in the dev environment
only because that environment still held a 1.1.7 install of a 2.0.0 tree**, where the entry
point did not exist. So yesterday's conftest was not a complement to the entry point, it
was a patch over a stale environment, and on a correctly installed machine — every user's —
it was a hard error.

Deleting the conftest fixed it, and the fixtures now load through the mechanism a user
actually gets. `hatch env remove build` brought the dev environment to 2.0.0, at which
point `importlib.metadata` reports the entry point for the first time.

Both new checks were then proved to fail when they should, not merely to pass: a probe fed
`check_installed_version` a fabricated 9.9.9 and `check_entry_points` a target that does
not resolve, and both reported.

**What was left undone.** CI still runs one interpreter per workflow (3.12), so 3.13 is
covered locally and not in CI. The `ruff` question (D-025) is measured but not decided, and
the docs build, the citation check and the coverage floors are still outstanding from this
same session's list.

**Measured.** The gate is green on **three interpreters**: 3.12, 3.13 and 3.14 — 131 passed
+ 1 xfailed, `mypy --strict` clean on 53 files, **16 checks** (was 14), 2 advisories, on
each. Gate wall time 3.7 s. `CLAUDE.md` 164 → 178 lines, budget 200.

---

## 2026-09-17 — A graph built from declarations, matching the one the decorators mutate

**What.** `core/injection/graph.py` (`ApplicationGraph`) and `core/injection/builder.py`
(`GraphBuilder`), both unused by the framework. `tests/core/test_builder.py` characterises
them against the class-attribute path.

**Areas.** `src/dependency/core/injection/{graph,builder}.py`, `tests/core/test_builder.py`,
`stubs/`.

**Why.** Step 4. The graph must be buildable from declarations, and *demonstrably
equivalent*, before the class-attribute path can be deleted.

Three findings worth keeping:

- **No declaration registry is needed at all.** Every declared module is a subclass of
  `ContainerMixin` and every declared component a subclass of `ProviderMixin`, and both
  live in `injection/` — so Python's own subclass links are the index, and the builder
  needs no import from `agrupation` or `declaration`. A class that was never imported has
  no subclass entry and is correctly invisible, which is exactly what an `imports.py` is
  for. The plan had assumed an explicit ledger might be required; it is not.
- **Binding must be scoped to what the build can reach**, not to everything declared in the
  process. The first version bound every component in the interpreter, which made
  `tests/core/test_validation.py` — two `@instance` on one component, deliberately — fail
  an unrelated test's build. Scope is now: declared under this build's roots, plus the
  transitive import closure. That is the same universe `ProviderExpansion._seed` already
  walks.
- **Reaching into `graph._nodes` from the builder** was the first shape and was wrong;
  `ApplicationGraph.add_node` is the method.

**Architecture.** ✅ Complies. Additive; nothing in the framework calls either class. The
duplicate-implementation `DeclarationError` is written and tested here, in isolation,
before anything depends on it.

**What went wrong on the way.** Besides the scoping bug above, nothing. Note the honest
labelling: `test_builder.py` is a **characterisation** test (`tests/CLAUDE.md`, fourth row)
— it records present behaviour, not desired behaviour, and is meant to die with the path it
characterises. The one exception is
`test_two_implementations_for_one_component_are_rejected`, which is a specification: that
behaviour does not exist in the old path, where the last `@instance` imported wins silently
(D-030).

**What was left undone.** Nothing reads the graph yet — `Entrypoint`, `InjectionResolver`
and `ProviderExpansion` still walk class attributes. The `ContextVar`, the two-phase
`Entrypoint` and `graph.provide()` are step 6, and the mechanical `X.injection` → `X.node()`
rename is step 5, which exists solely to keep step 6 reviewable.

**Measured.** A throwaway probe built the **real example application's** graph from specs
and compared it field by field against the decorator-built one: **5 roots, 5 modules, 12
components, 0 mismatches** across name, parent, imports, optional imports,
`strict_resolution` and bound implementation — while sharing **0 node objects** and **0
provider objects** with it. Gate: 131 passed + 1 xfailed (was 123), `mypy --strict` clean on
53 files, 14 checks. `hatch run build:example` still boots with 0 errors.

---

## 2026-09-17 — Declarations become frozen specs, written but not yet read

**What.** New `core/injection/spec.py` with `ModuleSpec`, `ComponentSpec` and
`ImplementationSpec` — frozen, slotted, tuples not sets. `@module`, `@component`,
`@instance` and `@product` now attach one to the class they decorate, **in addition to**
everything they already did. Nothing reads them yet. `tests/core/test_spec.py` pins their
contents against the decorator arguments.

**Areas.** `src/dependency/core/injection/spec.py`,
`src/dependency/core/declaration/{component,instance}.py`,
`src/dependency/core/agrupation/module.py`, `tests/core/test_spec.py`, `stubs/`.

**Why.** Step 3 of removing process-global declaration state, and the step that makes the
dangerous one reviewable: the graph has to be buildable from declarations before the
class-attribute path can be deleted.

Two design points worth keeping:

- **Specs live in `injection/`, not `declaration/`.** `declaration` may import `injection`;
  the reverse would invert that edge and hand `check_layering` a second cycle, which is a
  failure rather than an advisory.
- **A spec holds a provider *factory*, never a provider instance.** `standalone_provider`
  builds `providers.Singleton(cls)` at decoration time, and that singleton's cached object
  then outlives every rebuild — measured earlier: `Svc.provide()` returns the same object
  across two independent `Entrypoint` builds. A factory is called once per build and cannot
  do that.

**Architecture.** ✅ Complies. Additive only; both paths run side by side.

**What went wrong on the way.** Nothing broke, but writing the specs surfaced the MRO trap
the design depends on: a subclass of an implementation **inherits**
`__implementation_spec__`, so reading specs with `getattr` would count it as a second
declaration of the same component. Every read goes through `own_*` helpers that look only
in `cls.__dict__`, and `test_a_subclass_of_an_implementation_declares_nothing` is what keeps
that true.

Also fixed in passing: `imports`, `optional` and `provides` are typed `Iterable` and were
being iterated directly, so a generator would have been consumed by the first reader. They
are converted to tuples once, at the top of each decorator.

**What was left undone.** Nothing reads a spec. `GraphBuilder` and `ApplicationGraph` are
step 4, and until they exist the specs are unverified against reality — the tests assert
they match the decorator arguments, not that a graph built from them behaves like the
current one. That comparison is step 4's characterisation test.

**Measured.** 123 passed + 1 xfailed (was 114), `mypy --strict` clean on 51 files, 14
checks passed. `hatch run build:example` resolves in **0.0088 s** with zero errors,
`CancelInitialization` still skips the unfitted pressure probe, and shutdown is clean on
SIGINT — read from the output, not inferred from a green suite.

---

## 2026-09-17 — A pytest plugin that measures what it cannot yet isolate

**What.** New `src/dependency/testing/` subpackage, shipped deliberately incomplete:
a `dependency_container` fixture, a `declaration_state()` snapshot helper, the `testing`
extra, the `pytest11` entry point, a `testing` line in `LAYER_ALLOWED`, and
`tests/conftest.py` — the repository's first.

The load-bearing piece is `test_resolving_leaves_no_trace_on_the_declared_classes`, an
`xfail(strict=True)`. It asserts that resolving an application leaves the declared classes
untouched, which is **false today**. When declaration state stops being process-global it
becomes an xpass, `strict=True` turns that into a build failure, and whoever lands the
change is forced to delete the marker. The definition of done is a test rather than a
sentence.

**Areas.** `src/dependency/testing/`, `tests/testing/`, `tests/conftest.py`,
`pyproject.toml`, `tools/audit_dependency.py`, `stubs/dependency/testing/`.

**Why.** Step 2 of removing process-global declaration state.
`docs/roadmap.md` asks, as the question that decides whether the work is a fixture or a
redesign, *"is the declaration registry resettable at all?"* This answers it with a
measurement instead of an opinion: it is not.

**Architecture.** ✅ Complies. `testing` imports `core` and nothing in `core` imports
`testing`, so `KNOWN_CYCLES` still holds exactly one pair. No fixture is `autouse` — the
entry point loads this module in every environment where the package is installed, so a
plugin that changed behaviour on install would break somebody's suite on upgrade.

**What went wrong on the way.** The fixture was not found on first run. The `pytest11`
entry point lives in the metadata of an **installed** distribution, and this suite runs
against `PYTHONPATH=src`. Fixed by naming the plugin in `tests/conftest.py`, which is the
honest split: the conftest proves the fixtures work, and the `release` skill proves the
entry point registers, by installing the wheel into a clean venv.

**What was left undone.** **The entry point is unverified.** `importlib.metadata` in the
build env reports no `pytest11` entry for this package, and the installed distribution
there still says **version 1.1.7** while `pyproject.toml` says 2.0.0 — the dev environment
lags the source tree, which is this repository's named blind spot. Nothing here is proven
to work from a wheel until the `release` skill runs. Also: `dependency_app` does not exist
yet; it arrives with the graph in step 6.

**Measured.** 114 passed + 1 xfailed (was 111), `mypy --strict` clean on **50** source
files (was 48), 14 checks passed with 2 advisories — no new layering advisory, so the
`testing` layer is declared correctly.

---

## 2026-09-17 — The layering doc claimed a cycle that had been closed

**What.** Seven decision citations were wrong across four files. `core/CLAUDE.md` said
**two** cycles exist and cited D-016/D-017 (graphviz and forward references); there is one,
D-018, and the `core → library` cycle it described was closed by D-019 — `entrypoint.py`
imports `core.utils.threading`, not `library`. `KNOWN_CYCLES` has held exactly one pair all
along. Also: the name-collision rule cited D-018 in three places instead of D-020, and
`tests/CLAUDE.md` cited D-015 (the stubs decision) for the `--dist=loadfile` measurement
instead of D-023.

**Areas.** `src/dependency/core/CLAUDE.md`, `tests/CLAUDE.md`,
`tools/audit_dependency.py` (two docstrings).

**Why.** Found while verifying the layering before adding a `testing` layer in the next
step. A wrong citation is worse than none: it sends the reader to a decision that says
something else, confidently.

**Architecture.** ✅ Complies. No behaviour changed; the documents now match
`LAYER_ALLOWED` and `KNOWN_CYCLES`.

**What went wrong on the way.** Nothing, but the finding itself is the point: the audit's
own docstring was one of the wrong ones, so the check and the rule it enforces disagreed
about which rule that was.

**What was left undone.** No script checks that a `D-0xx` citation points at a decision
that exists, let alone the right one. A check that every cited number appears in
`docs/decisions.md` would be cheap and would have caught four of these seven.

**Measured.** Gate unchanged: 111 tests, `mypy --strict` clean, 14 checks passed.

---

## 2026-09-17 — Container configuration stops being process-wide

**What.** `Container.config` moved from a class-body assignment to per-instance assignment
in `__init__`. New `tests/core/test_container.py` with the two assertions that were false
before. D-043.

**Areas.** `src/dependency/core/resolution/container.py`, `tests/core/test_container.py`,
`docs/decisions.md`, `stubs/dependency/core/resolution/container.pyi`.

**Why.** Step 1 of removing process-global declaration state. `Container` extends
`DynamicContainer`, which does not copy providers per instance, so one `providers.
Configuration` object was shared by every container in the interpreter. The suite's whole
stated isolation boundary — one `Container` per test, D-023 — did not hold for
configuration, and nobody knew.

**Architecture.** ✅ Complies. It closes a gap in D-023 rather than changing it.

**What went wrong on the way.** Nothing in the fix. The bug itself had been invisible
because no test ever built two containers with different config and compared them — the
suite proved isolation for providers and assumed it for config.

**What was left undone.** `Plugin.config` is still a class attribute written by
`setattr` at build time (`plugin.py:64`), and the example reads it in public as
`SensorsPlugin.config.sensors.sample_interval_s`. That is the same family of problem and is
deliberately deferred to step 5 of the plan, when the builder exists and the real cost is
visible.

**Measured.** Before: `a = Container.from_dict({'x': 1})`, `b = Container.from_dict({'y': 2})`
gave `a.config is b.config` → `True` and `a.config()` → `{'x': 1, 'y': 2}`; `config` was not
in `container.providers` at all. After: distinct objects, `{'x': 1}` and `{'y': 2}`, and
`config` is a registered provider. Gate: 111 tests (was 109), `mypy --strict` clean, 14
checks passed.

---

## 2026-09-17 — Settle the version at 2.0.0, which unblocks the gate

**What.** `pyproject.toml` 1.1.7 -> 2.0.0, `tools/api_snapshot.json` rewritten as what
2.0.0 publishes (22 names: `Registry` out, `ExpansionFailure` and `ExpansionResult` in),
and `CHANGELOG.md`'s `[Unreleased]` section became `[v2.0.0]`.

**Areas.** `pyproject.toml`, `tools/api_snapshot.json`, `CHANGELOG.md`.

**Why.** Step 0 of the plan to remove process-global declaration state. Every later step
changes `dependency.core.__all__`, and under D-013 that is impossible to do honestly while
the version still claims to be the one that contained `Registry`. It was also the single
open decision blocking the whole roadmap.

**Architecture.** ✅ Complies. D-013 is satisfied rather than bypassed: the major bump is
what makes the already-shipped removal legal.

**What went wrong on the way.** Nothing. The failure this clears was deliberate and had
been red since the resolution refactor.

**What was left undone.** The migration guide the README has owed longest is still owed,
and nothing is published — this bumps the version, it does not cut a release. The `release`
skill has not been run.

**Measured.** The gate goes from **1 failure across 14 checks** to **14 checks passed, 2
advisories** — the first fully green audit of this session. 109 tests, `mypy --strict`
clean on 48 files.

---

## 2026-09-17 — The agent method goes from version 0 to version 7

**What.** Updated this repository's copy of the method from the single unversioned
`bootstrap-prompt.md` (version 0 by content: 13 principles, no session loop, no header) to
the four-document set at version 7, and applied the deltas that this repository actually
needs. Thirty-six deltas were listed across v1–v7; the triage took 14, found 11 already
here, and declined 3 with their reason recorded in the header.

- The header is carried forward in all four documents, identical in each: `adopted`
  2026-09-17, five `adapted` entries naming this repo's own shapes (the gate command, the
  audit script, the skill names, the session loop living in a skill, the docs exclusion),
  and three `declined` entries with reasons. D-040.
- `workflow` skill: the five missing steps of the session loop — the opening brief (§0),
  pick-and-price, the question protocol, looking at the output (§5), and the closing review
  with the harvest routing table (§8). The skill went 96 → 216 lines; it is on demand, so
  it costs nothing until a change starts.
- `CLAUDE.md`: three lines only — the opening brief, test-first, and a document-map row for
  `docs/agents/prompt-context.md`. 157 → 164 lines, inside the 200 budget. That row is not
  decoration: `check_document_map` now fails if the method set is moved or deleted.
- `tests/CLAUDE.md`: principle 18 with the four cases where test-first does not fit, and
  four test properties this repo had never written down.
- `.claude/logs/agent-changelog.md`: the format gained **What went wrong on the way** and
  **What was left undone**. Earlier entries are not rewritten.
- `docs/roadmap.md`: the five states declared and an entry with no marked state defined as
  *planned*; `## Tooling` became `## Process and tooling` with a first-hit friction list
  held below the promotion threshold; a new entry for a deprecation path.
- `docs/decisions.md`: D-040 (the set is updated by running `prompt-update.md`, never by
  pasting over it), D-041 (editing the method here **is** a fork), D-042 (a second agent
  surface would be generated, never hand-maintained).
- `verify` skill: the four evaluation layers this repo already had and never named.
  `state-review` skill: a seventh question — is the method header still honest?
- `docs/roadmap.md` §Process and tooling also gained the two entries that had no home
  anywhere else: the two learnings owed upstream to the method, written out in full so they
  survive this session, and the missing enforcer for the method header. Both were floating
  in a session report, which is the definition of a learning that dies with the context
  window.
- **Pruned `docs/agents/bootstrap-prompt.md`** (986 lines, read in full before the verdict).
  Every section is covered by the new set and was checked one by one, not by title: the
  enforcement ladder is carried over verbatim, principles 1–13 survive unrenumbered inside
  1–19, the nine phases moved to `prompt-bootstrap.md`, and the stack tables were verified
  piece by piece (GDScript, `sqlfluff`, Packwerk, *one gate command*, *pin the tooling
  versions*). The worked example is deliberately less specific now — v4 anonymised it, and
  the omission is the improvement. **It contained nothing about this repository**: zero
  occurrences of every noun of this project, so nothing had to be moved out. One inbound
  link exists, in this file's own 2026-09-17 bootstrap entry; it is session history and
  correctly describes what existed then, so it stays and this entry is what makes it
  navigable.

**Areas.** `docs/agents/`, `CLAUDE.md`, `tests/CLAUDE.md`, `docs/roadmap.md`,
`docs/decisions.md`, `.claude/skills/workflow`, `.claude/skills/verify`,
`.claude/skills/state-review`, this file.

**Why.** A newer copy of the method was dropped into `docs/agents/`. Overwriting without
triaging gives a repository whose method document describes practices it does not follow,
which is worse than being a version behind — it is being a version behind while claiming
not to be.

**Architecture.** ✅ Complies. No source file was touched; the gate's only failure is the
pre-existing, deliberate `api_snapshot` one.

**What went wrong on the way.** The new copies were dropped **on top of** the old one
instead of at a scratch path, which is the one thing the update procedure says not to do —
the old header is the only record of what a repository adapted and declined. It cost
nothing here only because the old file had no header at all and was still in `HEAD`. Also
found while writing the test properties: `tests/CLAUDE.md` still quoted the pre-D-029
coverage figure of 91%. Corrected to 78%, which is the number D-029 measured.

**What was left undone.** Three deltas were declined, not deferred: Workspaces (one repo),
Models and cost (it governs how the method is run, not what this repo guarantees), and the
pre-flight for this repo's own skills (they are short and reversible). The `digest` field
cannot be verified — the set defines what it is but never says how it is computed, so a
mismatched copy would not be detectable here. Two learnings are owed upstream rather than applied
locally, because editing the method here would be a fork (D-041): the
task-runner-is-an-untyped-surface rule, and *check the denominator before believing a
coverage number*. Both are written out in `docs/roadmap.md` §Process and tooling, with the
`digest` gap beside them — not left in a report. One section of the pruned file was **covered worse** rather than covered —
its argument that a document read once on demand may be long while a file loaded every
session must not be — and it is owed upstream for the same reason instead of being lifted
locally.

**Measured.** Gate after the change: 109 tests pass in 1.17s, `mypy --strict` clean on 48
files, audit 14 checks with 3 advisories and the one known `api_snapshot` failure that the
roadmap documents as deliberate until the version is bumped. Unchanged from before this
work — no check went from green to red.

---

## 2026-09-17 — Close out everything that needed no decision

**What.** Finished the four remaining roadmap items that were not blocked on a judgement
call, and rewrote the rest of the roadmap so every surviving entry names its blocker.

- `tests/core/test_wiring_contract.py`: the contract test against `dependency-injector`'s
  private `_Marker`. Asserts shape (names exist, `__class_getitem__`, `modifier`, deferred
  resolution) and behaviour (a wired injection resolves end to end). D-038.
- `tests/library/test_threading.py`: `excluded` under real contention, lock release after
  an exception, `threaded` off-thread and returning nothing, `handle_exit` not swallowing
  real exceptions.
- Enabled the pydantic mypy plugin in `.mypy.ini`. D-039.
- Recorded D-037 after the contract test found it.

**Areas.** `tests/core/`, `tests/library/`, `.mypy.ini`, `docs/decisions.md`,
`docs/roadmap.md`.

**Why.** Requested: finish what can be finished now, define the rest in the roadmap, and
close the session.

**Architecture.** ✅ Complies. No source change except the mypy configuration.

**Measured.**

- **`@inject` does nothing on a module-level function** — found while writing the contract
  test, which failed on its first run for exactly this reason. `ResolutionStrategy.wiring`
  passes `injectable.modules_cls`, which holds component *classes*, so dependency-injector
  wires those classes' members and nothing else. No error is raised: the marker object is
  passed through as the argument. Pinned by a test. D-037.
- **The pydantic mypy plugin produced zero new errors.** The roadmap entry predicted "a
  pile"; there was none. D-039.
- **`LazyWiring(_Marker, ABC)` does not fix the stub error.** `stubgen` emits the ABC base
  but not `metaclass=abc.ABCMeta`, and mypy still reports the abstract attributes.
  Reverted; the roadmap entry now records the attempt so nobody repeats it.
- Tests: **87 → 109**.
- State review: 14 checks defined = registered = cited by a rule; 39 decisions defined =
  cited; 3 rows still have `—` in the enforcer column; `CLAUDE.md` at 157/200 lines; no
  dead pointers in the document map.

**Left open, all blocked on a decision.** The version number (`2.0.0` vs a `1.2.0` with a
deprecation shim), `py.typed` versus generated stubs, the first-party pytest plugin, making
the `reference` collision unrepresentable, breaking the `injection ↔ resolution` cycle,
letting the root container see plugin providers, deterministic bootstrap order, `ruff`, and
the warning a plugin without config emits.

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
