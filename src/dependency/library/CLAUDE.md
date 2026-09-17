# library/ — batteries for applications built on the framework

Part of the product, but not the core. These are prebuilt pieces an application using
`dependency` will want: threading helpers, classic patterns, and dependency-graph
rendering. `src/example/` uses them, which is how they get exercised.

## Dependency rules

- `library/` may import from `dependency.core.injection` **only**. It must not reach into
  `declaration/`, `agrupation/` or `resolution/`. Today `graph/generate.py` respects this.
- `core/` importing back from `library/` is the accepted cycle D-017
  (`agrupation/entrypoint.py` → `library.threading.handle_exit`). Do not add a second one.

## Optional dependencies

`patterns/` and `threading.py` use only the standard library and are hard dependencies of
the package. **`graph/` requires `graphviz`, which is an extra**, installed with:

```bash
pip install module-dependency[graph]
```

Any module here that needs a package outside `[project.dependencies]` must:

1. declare it in `[project.optional-dependencies]`, and
2. fail with a message that names the extra, not with a bare `ModuleNotFoundError`.

This was not true before: `graph/` shipped in the wheel importing an undeclared
`graphviz`, so `from dependency.library.graph import generate_graph` failed for every
user who pip-installed the package. It was invisible from the source tree because the
dev environment has `graphviz` installed. Enforced in
`audit_dependency.py::check_declared_imports`.

## `patterns/` and `threading.py` have no tests

Coverage is 55% on both, and `graph/` has none at all. `if __name__ == '__main__'` demo
blocks in `patterns/observer.py` and `patterns/state.py` are the only exercise they get.
They are not runnable proof. See the roadmap.
