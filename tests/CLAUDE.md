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

## Known gap

`tests/cli/test_generation.py` calls all four generators and **asserts nothing**. It
passes while the templates emit code that raises `TypeError` on import. A generator test
must execute or at least `ast.parse` + signature-check what it generated, not merely
render it. Covered by `audit_dependency.py::check_cli_templates` until the test is fixed.

`src/dependency/library/graph/` is imported by **no test at all** — it does not even
appear as a row in the coverage report, while the total reads 91%.
