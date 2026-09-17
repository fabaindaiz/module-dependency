# core/ — the framework

Four subpackages. The split is by *phase of the lifecycle*, not by object type:

| Package | Owns | Runs at |
|---|---|---|
| `declaration/` | `@component`, `@instance`, `@product`, provider validation | import time |
| `agrupation/` | `Module`, `Plugin`, `Entrypoint` — structural grouping | import time |
| `injection/` | the tree (`ContainerInjection`/`ProviderInjection`), the binding (`Injectable`), wiring markers | import time, read at resolution |
| `resolution/` | expansion, topological resolution, wiring, bootstrap | `Entrypoint.initialize()` |

## Allowed dependency direction

```
declaration  ──▶  agrupation  ──▶  injection  ◀──▶  resolution  ──▶  utils
                                       ▲
                                    library
```

**One** cycle exists, and it is **accepted, not endorsed** — D-018:

- `injection ↔ resolution`: `injection/mixin.py` imports `resolution.container.Container`
  because `ContainerMixin.on_resolution` takes it in its signature. Breaking it means
  changing a public signature, so it is gated on a major version.

There was a second, `core → library`, and **it is closed** (D-019): `handle_exit` moved to
`core/utils/threading.py` and `library/threading.py` re-exports it, so `agrupation/
entrypoint.py` imports from `core.utils`, not from `library`. `library` is no longer in
`core.agrupation`'s allowed set.

`audit_dependency.py::check_layering` reports the accepted cycle as an **advisory**, and
`KNOWN_CYCLES` holds exactly that one pair. Do not add a second: a new one is a failure,
not an advisory. If you break the existing one, promote the check to a failure in the same
commit.

## The one thing to understand before changing resolution

`ProviderExpansion` (in `resolution/expansion.py`) is a four-step BFS, and its class
docstring is the contract — keep it in sync with the code or delete it:

1. **Seed** — implemented providers from the structural tree, plus `extra`.
2. **Expansion** — BFS through `imports` and `optional_imports`, discovering undeclared
   providers and adopting each into the container of whoever first imported it.
3. **Conditions** — required + no impl + strict → failure; required + no impl + not
   strict → skipped; optional + no impl → skipped, always.
4. **Cascade** — a provider with a failed *required* import also fails. Optional never
   cascades.

`should_resolve()` answers "can this be attached to the DI container" and returns
`False` for a missing implementation. `strict_resolution` controls *error reporting
during expansion*, not attachment eligibility. These two are routinely confused; the
docstring on `should_resolve` says so explicitly.

## Exemplary files

- New resolution logic → copy the shape of `resolution/expansion.py`: dataclasses for
  result types, a class that takes its inputs in `__init__` and exposes one verb.
- New diagnostics → `resolution/errors.py`.
- New decorator → `declaration/component.py`. Note the two-step shape: `init_injection`
  then `update_dependencies`, with the `issubclass` guard marked `# pragma: no cover`.

## Mistakes already made here

- **`container.check_dependencies()` validates nothing in this framework.** It only
  inspects `providers.Dependency`, which `validation._PROVIDERS` makes impossible to
  create. Measured: 0 such providers in the full example app tree. The call is kept for
  the `init_resources()` beside it. Do not add validation logic that assumes it works.
- **`partial_resolution` does not exist**, and never did as code. It survived in two
  docstrings after the refactor that removed it; both are now corrected. If it reappears
  in a document, that document is stale — do not implement the attribute to match it.
- **`ResolutionConfig.legacy_resolution`** switches `Entrypoint` to the pre-expansion path
  (`resolve_dependencies` in one call instead of `resolve_modules` then `initialize`). It
  defaults to `False` and exists for compatibility; new code should not rely on it.
- Provider `name` comes from `cls.__name__`, and `reference` is the dot-path built from
  the parent chain. Two same-named providers under one container silently overwrite via
  `setattr`. See D-020.
