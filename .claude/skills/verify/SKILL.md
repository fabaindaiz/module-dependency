---
name: verify
description: Run this project's gate and report honestly what passed. Use before saying a
  change is done, after touching core/resolution or core/injection, and whenever asked to
  "check", "validate", "run the gate", "is this ready", or "does this still work".
allowed-tools: Bash, Read
---

# Verify

This repo had four shipped bugs that every green test run missed, because the test suite
never imported the broken module and the gate never ran the type checker. Green is not the
same as verified.

## The four layers, and what each one answers

The gate is the floor, not the ceiling. This repo has all four layers; they answer different
questions, and a claim is only as strong as the layer that actually ran.

| Layer | Answers | Here |
|---|---|---|
| The gate | did we break a rule we already knew about? | `hatch run build:gate` |
| The invariant test | does the graph still validate before the first object is built? | `hatch run build:example`, which walks the full expansion path |
| The pre-ship check | does it work **in the artefact we actually ship**? | the `release` skill — wheel, clean venv, minimum Python |
| Looking at it | is what we produced any good? | read the example's log output, the generated file, the error text |

## The gate

```bash
hatch run build:gate
```

Runs `tests`, then `typecheck`, then `audit`, and stops at the first failure.

## What a failure means

| Failing step | What to do |
|---|---|
| `tests` | An actual regression. Read the assertion before changing anything |
| `typecheck` | `mypy --strict`. Not advisory — it was failing silently for a while because CI never ran it |
| `audit` — `version_floor` | `requires-python`, `.mypy.ini` and CI disagree about the minimum Python |
| `audit` — `forward_refs` | A class-body annotation names something defined later. Works on 3.14 only. Reorder the classes |
| `audit` — `declared_imports` | An import that is not in `[project.dependencies]` or a declared extra. This is the bug class this repo cannot see: it works here and fails for the user |
| `audit` — `stub_parity` | Run `hatch run build:stubs`. The stubs are the only type surface consumers get |
| `audit` — `docs_references` | A `::: path` in `docs/reference/` points at a deleted module. This fails the release docs job |
| `audit` — `cli_templates` | A template emits a decorator keyword that does not exist. The generated code would raise `TypeError` |
| `audit` — `api_snapshot` | A public name was removed without a major version bump. See D-013 |
| `audit` — `hatch_scripts` | A `hatch run` script calls something with the wrong arity |

## Advisories

Printed every run, stop nothing. Two are expected today:

- `layering` — the accepted `injection ↔ resolution` cycle (D-018).
- `name_collisions` — 27 duplicate class names across test files, harmless while each test
  builds its own `Container` (D-020, D-023).

**A third cycle is a failure, not an advisory.** Do not add one to the accepted list to
make the audit quiet.

## After touching resolution or injection

Also run the example app. It exercises the full expansion path end to end, which unit tests
only reach in pieces:

```bash
hatch run build:example     # blocks in main_loop — Ctrl-C once you see "Application initialized"
```

## If packaging changed

The gate does **not** build a wheel. If you touched `pyproject.toml`, `library/`, or added
any import, use the `release` skill instead.

## Reporting

Say what passed and what did not, with the output. Never call something verified that was
not run. Name the known-failing item explicitly so it is not presented as new — right now
`api_snapshot` fails on purpose until the version is bumped to `2.0.0`.
