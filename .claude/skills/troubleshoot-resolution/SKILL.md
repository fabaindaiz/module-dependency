---
name: troubleshoot-resolution
description: Diagnose startup and injection failures in this framework. Use when a
  ResolutionError, DeclarationError, ProvisionError or InitializationError is reported,
  when an application "does not start", when a dependency "is not injected" or is None,
  when a circular dependency is suspected, or when a provider resolves in the example app
  but not in a test.
allowed-tools: Bash, Read, Grep
---

# Troubleshooting resolution

This repo's failure knowledge is **not in the git history** — 212 commits, 25 saying `fix`,
none naming a symptom. It is in `CHANGELOG.md`, in a handful of docstrings that record a
decision, and in `src/example/`. This skill is built from those.

## Read the exception type first

| Exception | It means | Look at |
|---|---|---|
| `ResolutionError` from expansion | a required import had no implementation, or its dependent cascaded | the import chain in the message: `A → B → C`. C is the cause, A is who wanted it |
| `ResolutionError` from `injection` | the layer loop stalled: a cycle, or an unresolved import | `raise_resolution_error` logs cycles first. If no cycle is logged, it is a missing implementation |
| `DeclarationError` on `.provide()` | the provider was never resolved | whoever called `.provide()` did not declare it in `imports=` |
| `DeclarationError` on `.provider` | no implementation was ever assigned | no `@instance` for that component, and no inline `provider=` |
| `ProvisionError` | plugin config failed validation, **or** a provider with no parent tried to build a `reference` | the plugin's `config:` type hint, or a missing `module=` |
| `InitializationError` | a `bootstrap=True` provider's `__init__` raised | the wrapped `__cause__`; this is application code failing, not the framework |

## The four failures that actually happen here

### 1. "It is not injected" — the implementation was never imported

`@instance` and `@product` register **at import time**. A module nobody imports does not
exist as far as the framework is concerned.

Check the plugin's `imports.py` lists the implementation module, and that
`app/main/imports.py` lists that plugin's `imports.py`. Check the import happens **after**
`super().__init__(...)` and **before** `super().initialize()` — that ordering is
load-bearing and the error message will not tell you.

### 2. "It is not injected" — an individually imported function

`dependency-injector` cannot patch a function that was imported individually
(`from mod import func`). The injection silently does not happen; nothing raises.

Grep the file for `from .* import` of a *function* rather than a module. Import the module.
This is D-008 and it is documented upstream.

### 3. `Provide` instead of `LazyProvide`

The bare markers resolve their reference at import time, before the injection tree exists.
Always `LazyProvide` / `LazyProvider` / `LazyClosing` (D-009). Both `LazyProvide[X]` and
`LazyProvide(X)` are valid.

### 4. A component resolves in the example app but not in a test

Almost always the `Container`. Each test must build its own; sharing one between tests, or
attaching two same-named plugins to one container, makes the second silently overwrite the
first via `setattr` (D-020, measured). Symptom: a provider resolves to the wrong
implementation rather than raising.

## The distinction people get wrong

`should_resolve()` answers *"can this attach to the DI container"* and returns `False` when
there is no implementation. `strict_resolution` controls *error reporting during expansion*.
They are not the same switch, and the docstring on `should_resolve` says so. If you are
about to add `strict_resolution=False` to silence something, check which of the two you
actually mean.

## Reading the expansion result directly

When the message is not enough, run expansion by hand and inspect both halves:

```python
from dependency.core.resolution.expansion import ProviderExpansion
result = ProviderExpansion(modules=[MyPlugin], extra=()).expand()
print("resolved:", sorted(map(str, result.resolved)))
for f in result.failures:
    print(f.reason, "|", " -> ".join(map(str, f.node.import_chain())))
```

`raise_if_failed()` is what turns this into the exception; calling `expand()` yourself lets
you see the resolved set too.

## Turning on the framework's own logging

Every internal event goes to the `dependency.loader` logger at DEBUG:

```python
import logging
logging.getLogger("dependency.loader").setLevel(logging.DEBUG)
logging.basicConfig()
```

You will see orphan adoption, implementation assignment and reassignment, and skipped
optional providers — the three things that are otherwise invisible.

## What is a bug versus what is WIP

`partial_resolution` appears in two docstrings and in no code. If you are chasing it, you
are chasing a stale comment — fix the docstring rather than implementing the attribute.
Likewise `Registry` and `FallbackPlugin` were removed; any document mentioning them is out
of date, not describing a feature you cannot find.
