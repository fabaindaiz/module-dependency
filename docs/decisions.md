# Decisions

Everything settled, numbered. Numbers are **never reused and never renumbered** —
`CLAUDE.md`, the changelog and the roadmap cite them.

The fourth column is the one that matters. A decision with `—` in it **can be broken
silently**. That is allowed; it should be visible.

A decision is made once. If it is reopened with no new fact, the answer is this document.

## Resolution — the core invariant

The invariant everything else serves: **the entire dependency graph is validated before
the first user object is constructed. If it cannot be satisfied, the application does not
start, and the error names the offending provider and its import chain.**

| # | Decision | Why | Enforced in |
|---|---|---|---|
| D-001 | Resolution is total and eager, never lazy or partial | A long-running or embedded process must fail at startup, where a human is watching, not three hours in. Guice by contrast validates only declared bindings and defers the rest — we deliberately do more | `ProviderExpansion.expand`, `ResolutionStrategy.injection` |
| D-002 | A required import with no implementation fails; a provider with no implementation does not | They are different questions. `should_resolve()` answers "can this attach to the DI container"; `strict_resolution` controls error reporting during expansion. Conflating them either blocks valid optional interfaces or hides real gaps | `ProviderInjection.should_resolve`, `ProviderExpansion._enqueue_imports` |
| D-003 | Optional import failures never cascade | Resilience is explicit and bounded, not a blanket `try/except`. A provider that declared `optional=` stated it can run without | `ProviderExpansion._cascade_failures`, which walks `.imports` only |
| D-004 | Only `Singleton`, `Factory` and `Resource` may back a provider | Makes the unvalidatable provider **unrepresentable** rather than merely rejected | `validation._PROVIDERS` |
| D-005 | `container.check_dependencies()` is kept although it validates nothing here | It only inspects `providers.Dependency`, which D-004 makes impossible to construct. Measured: 0 such providers in the full example-app tree. Kept for the `init_resources()` call beside it | — |
| D-006 | The import chain is part of the contract, not a nicety | Without it, a missing provider names neither the importer nor the cause. This is the single most expensive diagnostic to lose | `ExpansionResult.raise_if_failed` |
| D-007 | `CancelInitialization` is the only sanctioned way to abort one component | A component may give up without taking the application down; any other exception means the graph is wrong | `ResolutionStrategy.initialize` |

## Wiring

| # | Decision | Why | Enforced in |
|---|---|---|---|
| D-008 | `imports.py` files import modules, never individual functions | `dependency-injector` cannot patch an individually imported function; the injection silently does not happen. Their documentation says so explicitly | — (see `docs/references.md`, wiring entry) |
| D-009 | Always `LazyProvide`/`LazyProvider`/`LazyClosing`, never the bare markers | The Lazy variants defer reference resolution to injection time. The bare ones resolve at import time, before the tree exists | `LazyWiring.__init__` |
| D-010 | `warn_unresolved=True` stays on | It is the only thing that reports a mistyped reference string. Added upstream in `dependency-injector` 4.48.2, which is why that is our floor | `ResolutionStrategy.wiring` |
| D-011 | `Component.provide()` is accepted although it is formally Service Locator | Seemann's objection is that Service Locator *"hides a class' dependencies, causing run-time errors instead of compile-time errors"*. We pay that back: `imports=` forces the declaration, and D-001 turns the run-time error into a startup error. Python has no compiler to do this; startup is ours. **ASSUMPTION — confirm this is an accepted deviation and not design debt** | `ProviderMixin.provide` raises `DeclarationError` |

## Packaging and compatibility

| # | Decision | Why | Enforced in |
|---|---|---|---|
| D-012 | Backward compatibility is a constraint: prefer the lowest dependency bound that works | `dependency_injector>=4.48.2,<5`, not `>=4.49.0`. 4.49.0 is only needed for Python 3.14; with a 3.12 floor, 4.48.2 is the real minimum. Demanding more breaks users for nothing | `[project.dependencies]` |
| D-013 | The public API is `dependency.core.__all__`; removing a name needs a major version | Nothing else protected it. `Registry` was removed after v1.1.7 with the version still at 1.1.7 — the check now reports that | `audit_dependency.py::check_api_snapshot` vs `tools/api_snapshot.json` |
| D-014 | Minimum Python is 3.12 | `typing.override` is 3.12+ (PEP 698) and is used in `injection/injection.py`. The package previously declared `>=3.11` and could not be imported there at all — measured on a clean 3.11 venv | `audit_dependency.py::check_version_floor` |
| D-015 | The `stubs/` `.pyi` files are the only type surface; they are generated, never hand-edited | PEP 561 ranks `-stubs` packages above inline annotations, and this package ships no `py.typed`, so inline annotations are ignored by consumers entirely. Hand-editing happened twice in this repo's history and drifted back both times | `audit_dependency.py::check_stub_parity`, `permissions.deny` on `stubs/**` |
| D-016 | `graphviz` is an extra (`[graph]`), not a hard dependency | `library/graph` is part of the product but not primordial. It shipped importing an undeclared `graphviz`, so it failed for every user who pip-installed — invisible from the source tree, where the dev env has it | `audit_dependency.py::check_declared_imports` |
| D-017 | Class-body annotations never forward-reference unquoted | Works only on 3.14 (PEP 649); raises `NameError` on 3.12 and 3.13. Measured on clean venvs of all three. Fixed by ordering `library/graph/models.py` bottom-up | `audit_dependency.py::check_forward_refs` |

## Structure — accepted debt

| # | Decision | Why | Enforced in |
|---|---|---|---|
| D-018 | The `injection ↔ resolution` cycle is accepted, not endorsed | `ContainerMixin.on_resolution` takes a `Container` in its signature. Breaking it means changing that signature, which is public. A **third** cycle is a failure, not an advisory | `audit_dependency.py::check_layering` (advisory) |
| D-019 | The `core → library` edge is accepted | `agrupation/entrypoint.py` uses `library.threading.handle_exit`. Real, small, and not worth a new module to break | `audit_dependency.py::check_layering` |
| D-020 | Provider `name` is `cls.__name__`, and two same-named providers under one container overwrite silently | Measured: two distinct `TPlugin` classes produce the identical reference `TPlugin.TService`, and the second wins via `setattr`. Harmless today because each test owns its `Container`. Making it unrepresentable is a roadmap item | `audit_dependency.py::check_name_collisions` (advisory) |
| D-021 | `src/example/` uses `camelCase`; `src/dependency/` uses `snake_case` | The example's method names are its published teaching surface. Not worth churning; **do not copy the style into the framework** | — |
| D-022 | `dependency.cli` is frozen but must stay usable | Its templates emitted `interface=` and `component=`, which no decorator accepts — the generated code raised `TypeError` on import while the test suite was green, because the test only rendered and asserted nothing | `audit_dependency.py::check_cli_templates` |

## Process

| # | Decision | Why | Enforced in |
|---|---|---|---|
| D-026 | Every released version has a `CHANGELOG.md` entry | v1.1.6 and v1.1.7 shipped without one, so the only narrative record of what changed stopped at v1.1.5 while two releases went to PyPI | `audit_dependency.py::check_changelog_version` |
| D-027 | A task-runner script must point at code that exists and is called correctly | `hatch run build:graph` called `generate_graph()` with its required `plugins` argument missing. Nothing ran it, so nothing noticed | `audit_dependency.py::check_hatch_scripts` |
| D-028 | Every directory holding modules is a regular package, never an implicit namespace package | `core/utils/` and `library/` had no `__init__.py`. mkdocstrings could not collect from them, so `utils` went undocumented; coverage could not discover them either, which inflated the reported figure by 13 points | `audit_dependency.py::check_package_markers` |

## Closed by measurement

| # | Decision | The number that closed it | Enforced in |
|---|---|---|---|
| D-023 | `--dist=loadfile` is **not** a test isolation mechanism | The suite passes serially in one process (48 tests, 0.18s), with `-n 1`, and with `--dist=load` which distributes per test. The docs confirm `loadfile` only co-locates a file's tests on one worker; with 18 files and 6 workers each worker runs ~3 files in one interpreter anyway. The real boundary is **one `Container` per test** | `tests/CLAUDE.md` |
| D-024 | `[tool.mypy]` in `pyproject.toml` was dead and has been deleted | Verified with `mypy -v`: `Config File: .mypy.ini`. Its `plugins = ["pydantic.mypy"]` never loaded and its `mypy_path` never applied. Deleting it changes no behaviour; enabling the plugin is a separate, riskier decision | — (see roadmap) |
| D-025 | No formatter or linter is adopted in this pass | Formatting 2941 LOC would bury the changes that matter under thousands of lines of diff. It is a roadmap item with its own commit, not a side effect | — |
| D-029 | The reported coverage figure was 91% and the real one is 78% | Adding the two missing `__init__.py` files made **127 previously-undiscovered statements** visible to coverage: all of `library/graph/` plus `patterns/composite.py` and `patterns/state.py`. The 91% was not a regression that happened; it was a number that had never been true | `hatch run build:coverage` |
