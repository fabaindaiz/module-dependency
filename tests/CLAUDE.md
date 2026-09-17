# tests/

## The isolation boundary is one `Container` per test — nothing else

Declaration is a **process-global import-time side effect**: `@component` and `@module`
mutate class-level state when the module is imported, and there is no teardown. Every
test file therefore declares plugins and components at module scope, permanently, for
the lifetime of the interpreter.

What actually keeps tests from interfering is that **each test builds its own
`Container`**. Follow that, and nothing else matters.

What does **not** protect you, despite appearances:

- **`--dist=loadfile` is not isolation.** It only guarantees that tests in one file run
  in the same worker. With 18 files and 6 workers each worker runs ~3 files in one
  interpreter, sharing the global state. Measured: the suite passes serially in a single
  process (0.18s), with `-n 1`, and with `--dist=load`. See D-015.
- **Unique class names are not the protection either.** There are 27 duplicate class
  names across test files today (`TPlugin` in 7 files). They are harmless *only* because
  each lives in a different `Container`. Put two of them in one container and the second
  silently overwrites the first — `reference` collides at `setattr`. See D-018.

## Writing a test

- Build a fresh `Container` in the test body, not at module scope.
- `Container.from_json(...)` takes a path relative to the process CWD. Prefer
  `Container.from_dict({"config": True})` — it has no CWD dependency.
- Copy `tests/core/test_expansion.py`. It is the clearest example: scenarios separated by
  comment banners, one plugin per scenario with a scenario-prefixed name (`ExpA*`,
  `ExpB*`), and a docstring on each test stating the behaviour under test.
- Prefix new declarations with something scenario-specific rather than reusing `T*`.
  It costs nothing and removes the whole class of collision above.

## The test is written first

An agent that writes the code first writes **the test the code passes**: it has just spent
its attention deciding what the code does, and that is the wrong frame for deciding what it
*should* do. Test-after does not merely miss the defect — it **ratifies** it, and puts a
green assertion in front of it.

So: **red first.** Write the assertion and watch it fail *for the reason you expect*. A test
that passes before the code exists is testing nothing. Then the smallest change that makes
it pass. Then refactor, which is the only moment in the cycle where rewriting is safe.

Where that genuinely does not fit, say which row you are in:

| Case | What replaces the failing test |
|---|---|
| Exploratory spike — what is even possible with `dependency-injector` | a throwaway probe, deleted, and the real work then begins at red |
| Generated code | `ast.parse` plus a signature check of what was rendered — see *Known gap* |
| A one-off migration or script | a dry run against the real tree, and a review of the diff it would make |
| Code with no seam to test against | a characterisation test of current behaviour **first**, written to pass, and labelled as what it is |

That last row is the one legitimate test-after, and it is legitimate precisely because its
job is to record what the code does rather than what it should. Label those; never let them
be read as specifications.

**A bug fix starts with the test that reproduces it**, and that test keeps the decision
number in its name. It is the cheapest regression guard in existence and the one most often
skipped in the relief of having found the bug.

## Four properties worth keeping

- **Assert behaviour, not implementation.** If renaming a private helper breaks it, it is a
  change detector, not a test: it will fail on every honest refactor and be deleted in
  frustration, taking its real coverage with it.
- **One reason to fail per test.** When it goes red, the name should be enough to know what
  broke. Nine assertions look thorough and tell you none of them.
- **The name is the specification.** `test_required_import_without_implementation_aborts`
  beats `test_expansion_2`. It is read in the failure output, at speed, by someone who did
  not write it.
- **No sleeps, no real clock, no live network, no shared mutable fixtures.** Every one of
  these produces a suite that fails sometimes, and a suite that fails sometimes is a suite
  that gets re-run rather than read.

**Coverage is a smoke detector, not a goal — and check its denominator before believing the
number.** Two missing `__init__.py` files once hid 127 statements from the report entirely,
which turned a real 78% into a reported 91% (D-029).

## Known gap

`tests/cli/test_generation.py` calls all four generators and **asserts nothing**. It
passes while the templates emit code that raises `TypeError` on import. A generator test
must execute or at least `ast.parse` + signature-check what it generated, not merely
render it. Covered by `audit_dependency.py::check_cli_templates` until the test is fixed.

`src/dependency/library/graph/` is imported by **no test at all**: `library/` sits at 23%
and `graph/` at 0, against 95% on `core/`. The 91% this file used to quote was the inflated
figure from before D-029; the honest total is 78%.
