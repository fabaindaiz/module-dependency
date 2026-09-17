---
name: workflow
description: How to make a change in this repository, from locating the right layer to
  committing it. Use when starting any code change, when asked "where does this go",
  "how do I add a component / provider / module", or before opening a pull request.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Making a change here

## 1. Locate the layer before writing anything

| You are adding… | It goes in |
|---|---|
| a declaration rule or decorator | `core/declaration/` |
| a structural unit | `core/agrupation/` |
| tree, binding or wiring-marker logic | `core/injection/` |
| expansion, ordering, diagnostics | `core/resolution/` |
| a generic algorithm with no framework types | `core/utils/` |
| a reusable piece for applications *using* the framework | `library/` |
| a generator or template | `cli/` |

The allowed direction between these is in `src/dependency/core/CLAUDE.md`. Two cycles are
accepted (D-018, D-019); a third fails the audit.

## 2. Extend before creating

A second module doing a first module's job is how this codebase forgets what it decided.
Before adding a file, grep for what already does the job. If a new file is genuinely right,
say why in the commit.

## 3. Copy the exemplary file

- resolution logic → `core/resolution/expansion.py`
- diagnostics → `core/resolution/errors.py`
- a decorator → `core/declaration/component.py`
- a test → `tests/core/test_expansion.py`
- a plugin → `src/example/plugin/hardware/`
- a generator → `cli/generation/component.py`

## 4. Keep the paired artefacts in step

These pairs are one contract split across two files. Changing one without the other is a
silent break:

| If you change… | Also change |
|---|---|
| any signature in `src/dependency/` | `stubs/` — run `hatch run build:stubs` |
| a decorator in `core/declaration/` | the matching `cli/templates/*.j2` |
| the `ProviderExpansion` behaviour | its class docstring, and `docs/architecture.md` |
| `dependency.core.__all__` | `tools/api_snapshot.json`, and the major version if a name was removed |
| a module path | `docs/reference/core.md`, or the docs build fails on release |
| a rule in any `CLAUDE.md` | the matching check in `tools/audit_dependency.py` |

## 5. Run the gate

```bash
hatch run build:gate
```

Use the `verify` skill for what each failure means. If packaging or imports changed, use
`release` instead — the gate does not build a wheel.

## 6. Log it

Append to `.claude/logs/agent-changelog.md`, newest first:

```markdown
## YYYY-MM-DD — <one-line title>
**What.** What changed, concretely.
**Areas.** Files or folders.
**Why.** The reason, including the request that prompted it.
**Architecture.** ✅ Complies · ⚠️ Deviation · REVIEW — and why.
**Measured.** The number, if a claim was made.
```

This exists because two sessions refactored resolution here without seeing each other, and
three documents kept describing classes that had been deleted.

`CHANGELOG.md` is different: one entry per **released version**, user-facing.

## 7. Commits

Offer them; do not create them unless asked. Split by unit of change, not by file.

The message names the symptom or the decision. This repo has 212 commits, 25 of which say
`fix` — `fix mypy types`, `fix bootstrap`, `fix app start` — and not one names what broke.
Do not add to that. `wip` is not a message.

A commit that touches `src/dependency/` and leaves `stubs/` stale does not pass.

## If a request conflicts with a constraint

Architectural integrity overrides the request. State the cost, propose the correct path,
and deviate only on explicit confirmation. If confirmed, log it as **⚠️ Deviation** — not
as compliance.
