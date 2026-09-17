---
name: workflow
description: How to make a change in this repository, from locating the right layer to
  committing it. Use when starting any code change, when asked "where does this go",
  "how do I add a component / provider / module", or before opening a pull request.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Making a change here

The two bookends are **§0** and **§8**. They are the ones that get skipped, and they are
what makes one session useful to the next instead of only to this one.

## 0. The opening brief — before you touch the request

Read these before answering, before planning, and before agreeing that the request makes
sense. Stop as soon as a source has nothing to add.

- **In motion** — `docs/roadmap.md` §Where we are, and the last few entries of
  `.claude/logs/agent-changelog.md`.
- **In the tree** — uncommitted and staged changes. Some of it may be another session's
  work, and none of it is yours to fold in.
- **Constrains today** — the rows of `docs/decisions.md` that bear on the area the request
  touches. Read the *why*, not just the rule; you will be tempted to re-open it in an hour.
- **Stale** — a number from before a refactor, a `docs/references.md` entry whose upstream
  may have shipped, a document naming a file you should confirm still exists.
- **Friction still open** — `docs/roadmap.md` §Process and tooling.

Then say it, in six lines. **A line with nothing in it says `nothing`** — an omitted line is
ambiguous between *checked and clean* and *did not check*, and the reader cannot tell which.

```
In motion    <what is half-finished>
In the tree  <uncommitted work, and whose it is>
Constrains   <the decisions and numbers that bear on this request>
Stale        <what must be re-checked before it is trusted>
Changes it   <how the above alters the request — one sentence>
Friction     <open process items this work will touch>
```

`Changes it` is the point of the exercise. If the state of the repo does not alter the
request, say so plainly — "nothing here changes what you asked" is information.

### Pick from the roadmap, and price it before touching anything

Do not start with the most interesting item. Rank the candidates on the two axes this repo
can actually see — `docs/roadmap.md` §What each idea costs the core invariant, and whether
the gate can verify it — and report the ranking before building. Sort each into **Ready**,
**Blocked on a decision that is the human's** (name the decision), or **Blocked outside**
(say what would reopen it). Also name what you would *not* take, and why: that reason
usually outlives the session.

### Ask the few decisions, all at once, before writing

Theirs when different answers produce **materially different work**. Yours when there is a
conventional default, when a document here already answered it, or when it is reversible in
ten minutes — then pick, say which in one line, and keep going.

- **Ask before writing, and ask them together.** A question that arrives mid-work has
  already been answered by the code.
- **Price every option in this repo's own units**: providers walked at startup, statements
  covered, the Python floor, a name entering or leaving `dependency.core.__all__`, a third
  cycle in the layering. Never "more complex".
- **Say what each option forecloses**, and keep *do nothing* on the table.
- **Lead with a recommendation**, and cap it at three. Four options and no opinion is the
  work, undone.

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

### Then look at what you made

A green gate says the code did what it was told. It does not say that what it was told was
right. Produce the output and read it: run `hatch run build:example` and read the log lines
as an operator would at 3am; run the CLI generator and open the file it wrote; make a graph
unsatisfiable on purpose and read the error it actually prints, not the assertion that one
was raised.

- **A rare branch your change makes reachable is now yours.** It has never been seen.
  Exercise it once, deliberately, and look.
- **Distinguish silences that look identical.** "Not injected because the import was
  optional and absent" and "not injected because wiring never happened" are the same `None`
  and completely different bugs. If both are possible, say in words which one it is.

## 6. Log it

Append to `.claude/logs/agent-changelog.md`, newest first:

```markdown
## YYYY-MM-DD — <one-line title>
**What.** What changed, concretely.
**Areas.** Files or folders.
**Why.** The reason, including the request that prompted it.
**Architecture.** ✅ Complies · ⚠️ Deviation · REVIEW — and why.
**What went wrong on the way.** What the first attempt got wrong, and what caught it.
**What was left undone.** Debt this change created or walked past, named.
**Measured.** The number, if a claim was made.
```

The last three fields are the ones that pay for the file. A log of successes is bookkeeping;
one that names the wrong turn is what stops the next session taking it.

This exists because two sessions refactored resolution here without seeing each other, and
three documents kept describing classes that had been deleted.

`CHANGELOG.md` is different: one entry per **released version**, user-facing.

## 7. Commits

Offer them; do not create them unless asked. Split by unit of change, not by file.

The message names the symptom or the decision. This repo has 212 commits, 25 of which say
`fix` — `fix mypy types`, `fix bootstrap`, `fix app start` — and not one names what broke.
Do not add to that. `wip` is not a message.

A commit that touches `src/dependency/` and leaves `stubs/` stale does not pass.

## 8. Report, then close the session

**The report, in this order.** Never drop a constraint, a cost or a caveat to make it
shorter: what varies is order and emphasis, never inclusion.

1. **What is true now** — what was built, and whether it works. One or two lines.
2. **What it cost, and what it forecloses**, in this repo's own units.
3. **What you need from the human** — the structural decision you declined to take, the
   question you could not answer. Separate and unmissable; it is the part they must act on.
4. **The mechanism**, for whoever wants it: how it works, what was measured, what was
   rejected and why.
5. **What you did not do** — always, even when the answer is "nothing was left out".

Identifiers, commands, types, paths and error strings stay in English exactly as written,
whatever language the prose around them is in. A translated command does not run, and a
translated symbol cannot be grepped.

**A. Re-run what this change invalidated.** Did a measurement recorded elsewhere just become
wrong? Did this settle a question that was open — then a row in `docs/decisions.md` with the
enforcer column filled. Did it **unblock** something the roadmap calls blocked — change that
entry's state now, while you still know why. Did it make a rung-1 rule checkable — write the
check in `tools/audit_dependency.py`, or add it to §Process and tooling.

**B. Harvest, and route each learning to its home.** The question is not "did I learn
something"; it is **what does this session know that the repository does not?**

| What you learned | Where it goes |
|---|---|
| A question is now settled | `docs/decisions.md`, with its enforcer |
| A number, and how you got it | the document that owns that number |
| An external fact that changed or confirmed a decision | `docs/references.md`, with what we do differently on purpose |
| A rule a script could check | `tools/audit_dependency.py`, and note the rung it moved to |
| A trap that will be hit again | root `CLAUDE.md` if it is always relevant, the area `CLAUDE.md` if it is local |
| A procedure performed more than twice | a skill |
| Friction, hit for the second time | `docs/roadmap.md` §Process and tooling, with the arithmetic |
| A plan whose conditions changed | that roadmap entry's state |
| Something true only of this change | the changelog entry — that is a complete answer, not a failure |

**C. Capture is unconditional; proposing is throttled.** Always capture, every session,
without judging whether it matters — it costs seconds, and a learning not written down when
it happens is gone. Surface a *proposal* only when the friction has been hit a second time,
the human asked, or `state-review` is running. In the report the whole thing is one line:
`Captured: 3 learnings, 1 friction (2nd hit — see roadmap). Nothing needs you.`

**The closing question, asked plainly:** if the next session is a different agent with no
memory of this one, what would it have to re-derive? Whatever answers that is a gap you can
close in two minutes now and will never close as cheaply again.

## If a request conflicts with a constraint

Architectural integrity overrides the request. State the cost, propose the correct path,
and deviate only on explicit confirmation. If confirmed, log it as **⚠️ Deviation** — not
as compliance.
