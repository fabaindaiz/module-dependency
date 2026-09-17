# External information worth knowing

Not a link list: every entry says what it contributes **to this project**, and when it
contradicts something already decided, it says that too.

Rule for keeping it: something enters when it **changed or confirmed a decision**, not
because it is well written. An entry that produced no decision does not belong here.

---

## The framework we are built on

- **[Wiring — Dependency Injector](https://python-dependency-injector.ets-labs.org/wiring.html)** —
  how `Provide[...]` markers work, and what `container.wire()` actually patches.

  **What it confirms:** two of our central design choices, with a quotable reason for
  each. *"Python has a limitation on patching individually imported functions. To protect
  from errors prefer importing modules to importing individual functions or make sure
  imports happen after the wiring."* That is the entire justification for the `imports.py`
  convention (D-008) **and** for `LazyProvide` existing at all (D-009) — the Lazy markers
  are the "make sure imports happen after the wiring" half. It also documents dot-separated
  string identifiers (`Provide["services.user"]`), which is exactly the shape
  `ProviderInjection.reference` produces.

  **What we do differently, on purpose:** we never expose the bare markers. Every public
  example uses the Lazy variants.

  **Not applied yet:** the `packages=` argument to `wire()` recurses a package tree. We
  wire module-by-module from `injectable.modules_cls`. Worth revisiting only if wiring
  time shows up in a measurement — it has not been measured.

  Produced: D-008, D-009.

- **[Check container dependencies](https://python-dependency-injector.ets-labs.org/containers/check_dependencies.html)** —
  *"raises an error if container has any undefined dependencies"*.

  **What it confirms:** nothing we needed. **What it killed:** the belief that this call
  is part of our validation. It only inspects `providers.Dependency` providers, which
  `validation._PROVIDERS` makes impossible to construct here. Measured: 0 such providers
  in the entire example-app container tree. The validation burden is entirely ours.

  Produced: D-005. **Do not add logic that assumes this call validates anything.**

- **[Changelog](https://python-dependency-injector.ets-labs.org/main/changelog.html) and
  [releases](https://github.com/ets-labs/python-dependency-injector/releases)** —
  version history.

  **What it confirms:** `warn_unresolved` arrived in **4.48.2** and Python 3.14 support in
  **4.49.0**. That is where our dependency floor comes from, and why it is 4.48.2 rather
  than the newest (D-012).

  **Watch out:** release *dates* differ between the changelog page and the releases page
  (one reports 4.49.0 in 2025, the other in 2026). Version ordering and feature
  attribution are consistent; **do not cite the dates**.

  Produced: D-010, D-012.

- **[Issue #791 — "Current Maintenance Status and Future Plans"](https://github.com/ets-labs/python-dependency-injector/issues/791)** —
  a user asking, in March 2024, whether the project is alive, noting *"the last update was
  two years ago"*. **No reply.**

  **Why this is here:** search summaries confidently report that the project is "actively
  maintained again after an earlier hiatus". The primary source shows an unanswered
  question. Releases have since resumed, so the practical answer is yes — but the hiatus
  was real, and we depend on this project's **private API** (`_Marker`, imported in
  `injection/wiring.py`).

  **Not applied yet:** a contract test asserting that `_Marker`, `Modifier`, `Provide`,
  `Provider` and `Closing` still have the shape `LazyWiring` assumes. Today a refactor
  upstream would be discovered by our users, not by us. This is the highest-value item on
  the roadmap.

  Produced: D-012, and the `<5` upper bound.

---

## Python: the language and the packaging

- **[PEP 698 — `typing.override`](https://peps.python.org/pep-0698/)** — `Python-Version: 3.12`.

  **What it confirms:** the measured failure. `injection/injection.py` imports
  `typing.override`, so the package could never be imported on 3.11 despite declaring
  `requires-python = ">=3.11"`.

  **Watch out:** the PEP itself says nothing about a `typing_extensions` fallback. If
  anyone ever proposes lowering the floor back to 3.11, that needs verifying first — it is
  not established by this source.

  Produced: D-014.

- **[PEP 649 — deferred evaluation of annotations](https://peps.python.org/pep-0649/)** —
  `Python-Version: 3.14`. *"Annotations can access module-level definitions, class-level
  definitions, and even local and free variables."*

  **What it confirms:** why `library/graph/models.py` imported fine locally and raised
  `NameError` on 3.12 and 3.13. The local dev interpreter was 3.14.

  **What we do differently, on purpose:** we do **not** rely on it and do not use
  `from __future__ import annotations` either. `models.py` is simply ordered bottom-up so
  every annotation names something already defined. That keeps working when PEP 649 is
  universal and needs no `model_rebuild()`.

  Produced: D-017.

- **[PEP 561 — distributing type information](https://peps.python.org/pep-0561/)** — the
  precedence order a type checker uses.

  **What it confirms:** our unusual setup is correct, and correct for a reason we had not
  written down. Stub-only packages *"SHOULD supersede any installed inline package"*, and
  inline annotations require a `py.typed` marker we do not ship. So `dependency-stubs/`
  wins at step 3 and our inline annotations are ignored at step 4.

  **The consequence:** regenerating stubs is not housekeeping, it is the only way a type
  improvement reaches a user. Stale stubs mean every consumer checks against a lie.

  **Not applied yet:** adding `py.typed` and dropping the stubs entirely. That would be
  simpler, but it is a compatibility decision, not a cleanup.

  Produced: D-015.

- **[Writing pyproject.toml — PyPA](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)** —
  extras syntax and `requires-python`.

  **What it confirms:** the `[graph]` extra shape for D-016, including the combined-extra
  trick (`all = ["module-dependency[graph]"]`) that avoids a hand-maintained duplicate list.

  **Watch out:** version `classifiers` are *"only used for searching and browsing projects
  on PyPI, not for installing"*. Ours say only `Programming Language :: Python :: 3`, so
  there is nothing to keep in sync — and nothing gained either.

  Produced: D-016.

- **[pytest-xdist — distribution modes](https://pytest-xdist.readthedocs.io/en/stable/distribution.html)** —
  what `--dist` actually guarantees.

  **What it killed:** the belief that `--dist=loadfile` isolates tests. It only guarantees
  that *"all tests in a file run in the same worker"*. It says nothing about files being in
  different processes — with 18 files and 6 workers, each worker runs about three files in
  one interpreter, sharing our process-global declaration registry.

  Confirmed by measurement: the suite passes serially in one process (0.18s), with `-n 1`,
  and with `--dist=load`.

  Produced: D-023.

---

## The domain: dependency injection containers

- **[Composition Root — Mark Seemann](https://blog.ploeh.dk/2011/07/28/CompositionRoot/)**
  and **[Service Locator is an Anti-Pattern](https://blog.ploeh.dk/2010/02/03/ServiceLocatorisanAnti-Pattern/)**.

  **What it contradicts, head-on:** *"A DI Container should only be referenced from the
  Composition Root. All other modules should have no reference to the container."* We
  violate this centrally and deliberately. `Component.provide()` inside an `__init__`, and
  `LazyProvide` markers throughout application code, are exactly the access Seemann
  prohibits.

  **What we do differently, on purpose, and why it is defensible:** his stated harm is
  that Service Locator *"hides a class' dependencies, causing run-time errors instead of
  compile-time errors"*. Neither half applies here. Dependencies are **not hidden** —
  `imports=` makes them a declaration the framework reads. And the run-time error is
  **moved to startup** by D-001. Python has no compiler to give the feedback Seemann wants;
  our startup is that compiler.

  **Not applied yet:** constructor injection as the primary style. It would satisfy the
  pattern honestly, and it would be a different framework.

  Produced: D-011. **Without this entry, every well-read session will propose migrating
  away from `provide()` and will not be wrong on the theory — only on the trade-off.**

- **[Guice — Bootstrap / Stages](https://github.com/google/guice/wiki/Bootstrap)** — how
  the reference container in the field handles startup validation.

  **What it confirms:** eager instantiation as a fail-fast device is standard practice —
  `Stage.PRODUCTION`: *"All singletons are created"*. Our `bootstrap=True` is the same idea.

  **What we do differently, on purpose:** Guice does **not** validate the whole graph up
  front. Its Phase 1 validates only explicitly declared bindings; anything reached by
  just-in-time binding is checked when it is needed. We always expand the full transitive
  graph and always fail at startup. For embedded and long-running targets that is the right
  trade, and it is a deliberate departure from the most-cited implementation in the field.

  **Not applied yet:** Guice separates *validating* from *instantiating* via stages. We have
  no validate-without-instantiate mode. It might be worth having for tests.

  Produced: D-001.

- **The Python DI landscape** — `dishka`, `wireup`, `svcs`, `injector`, `modern-di`.
  **ASSUMPTION: download figures come from a search summary, not from a PyPI endpoint.**

  **What it confirms:** we are not redundant. The modern contenders compete on type-based
  autowiring and nested request scopes — the shape of a web service. None targets
  hierarchically grouped plugins with typed per-plugin config resolved totally at startup.

  **What we should copy:** `dishka` and `modern-di` ship a **first-party pytest plugin**.
  Our test-isolation story (D-023) is the problem such a plugin solves elsewhere, and
  "testing framework integration" has been in the README's Future Work for a while.

  **What produced nothing:** `injector`, `kink` and `punq` were reviewed for anything on
  total startup validation or plugin grouping. **Nothing found.** They are listed at the
  bottom of this file as alternatives; they are not sources of design guidance. Recording
  that here so nobody evaluates them a third time.

---

## What to read first

| If you are about to touch… | Read | And watch out for |
|---|---|---|
| `core/resolution/` | D-001 … D-007, the Guice entry | Total eager validation is the product, not an implementation detail |
| `core/injection/wiring.py` | the Wiring entry, Issue #791 | You are using a private upstream API (`_Marker`) with no contract test |
| anything that adds an import | the PyPA entry, D-016 | The dev env has packages the wheel does not declare |
| `library/graph/` | PEP 649, D-017 | Annotation order is load-bearing below Python 3.14 |
| `stubs/` | PEP 561, D-015 | Generated. Never hand-edit. They are the *only* type surface |
| `tests/` | the pytest-xdist entry, D-023 | `--dist=loadfile` is not isolation; one `Container` per test is |
| anything in `dependency.core.__all__` | D-013 | Removing a name is a major version bump |
| proposing to remove `provide()` | the Seemann entries, D-011 | The theory is right and the trade-off was made knowingly |

---

## Alternatives, for orientation only

Not sources of guidance — see the landscape entry above.

- [python-injector/injector](https://github.com/python-injector/injector)
- [reagento/dishka](https://github.com/reagento/dishka)
- [kodemore/kink](https://github.com/kodemore/kink)
