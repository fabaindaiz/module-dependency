---
name: state-review
description: Periodic health check of this repository's own instruction system — whether the
  documents still match the code, whether every rule still has an enforcer, and whether the
  root CLAUDE.md has drifted past its budget. Use when asked to "review the state", "check
  the docs", "is CLAUDE.md still accurate", or on a recurring schedule.
allowed-tools: Bash, Read, Grep
---

# State review

Bootstrapping is not the end. This system rots in a predictable way: agents delete code
faster than they re-read prose, so the documents drift first and nobody notices until a
release fails. That is exactly what happened here — `registry.py` was deleted and three
documents kept describing it until the docs build broke.

Answer all six. Report honestly; a clean review that skipped a question is worse than a
messy one.

## 1. Does every document in the map exist, and is every claim in it still true?

```bash
hatch run build:audit      # check_document_map and check_docs_references cover existence
```

Existence is checked. **Truth is not.** Spot-check by grepping the documents for class
names and verifying they still exist:

```bash
for name in $(grep -ohE '`[A-Z][A-Za-z]+`' docs/*.md | tr -d '`' | sort -u); do
  grep -rq "class $name\b" src/ || echo "STALE? $name"
done
```

## 2. Does every rule still have an enforcer, and did any fire this period?

Read the fourth column of `docs/decisions.md`. For every row naming a check, confirm the
check still exists in `tools/audit_dependency.py`:

```bash
grep -oE 'check_[a-z_]+' docs/decisions.md CLAUDE.md src/**/CLAUDE.md tests/CLAUDE.md \
  | sort -u | while read -r _ c; do grep -q "def ${c#*:}" tools/audit_dependency.py \
  || echo "RULE NAMES A CHECK THAT DOES NOT EXIST: $c"; done
```

Count the rows with `—`. Those are the rules that can be broken silently. If that number
grew, say by how much.

## 3. What changed that should have become a decision row and did not?

```bash
git log --oneline $(git describe --tags --abbrev=0)..HEAD
```

For each commit that changed behaviour, ask whether `docs/decisions.md` explains it. A
decision made in a commit message is a decision that will be re-litigated.

## 4. What in the roadmap is now closed — built, or closed by measurement?

Read `docs/roadmap.md`. Move anything built into `CHANGELOG.md`, and anything killed by a
number into **Closed by measurement**, *with the number*. An idea retired without its number
comes back next quarter.

## 5. Has the root `CLAUDE.md` drifted past budget, and which section grew?

```bash
wc -l CLAUDE.md          # budget: 200
```

If it is over, the growing section has become a document. Move the detail out and leave a
pointer — do not trim by deleting consequences or enforcers, which is what makes a rule a
wish.

## 6. Which rules are still on rung 1, and could cheaply be promoted?

A rule in prose with no enforcer is rung 1. A rule with an automated check is rung 3. A rule
the format makes unrepresentable is rung 4.

Current rung-1 rules worth revisiting:

- **D-008** (`imports.py` imports modules, never functions) — no enforcer. An AST check
  looking for `from X import <lowercase_name>` inside any `imports.py` would be cheap.
- **D-009** (always the Lazy markers) — no enforcer. A grep for bare `Provide[`/`Provider[`
  outside `injection/wiring.py` would be cheap and exact.
- **D-020** (same-named providers overwrite silently) — advisory only. Rung 4 is on the
  roadmap.

## 7. Is the method set itself still current, and is its header honest?

The four documents in `docs/agents/` carry one header, identical in all four. Check three
things, in this order:

- **The header is the same in all four files.** A file whose header disagrees with its
  siblings is worse than one with no header, because the update trusts it.
- **`adapted` and `declined` still describe this repository.** Every renaming we made and
  every delta we refused is in there with its reason. An adaptation that is not written
  down gets re-proposed by the next update, and re-declined, forever (D-040).
- **Nothing edited the method in place.** Changing those documents here is a fork and is
  done as one (D-041). If a diff touched them without bumping `ancestry`, that is a finding.

When a newer copy exists, `prompt-evaluate.md` is read-only and says whether this repo needs
`prompt-update.md`. Run it here rather than in the middle of a feature: updating the method
*after* the work means the work was done under the old method.

## Reporting

One section per question, with the command output. End with: how many rules are on rung 1,
how many decision rows have `—`, and whether the root file is within budget. Those three
numbers are the health of the system.
