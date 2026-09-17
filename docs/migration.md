# Migrating from 1.1.7 to 2.0.0

This release removes a public name, changes two behaviours you may be relying on, and adds
a command-line tool and a pytest plugin. Nothing is deprecated first — see
*[No deprecation path](#no-deprecation-path)* below, which is a deliberate policy rather
than an oversight.

Work through the four sections in order. The first two are the only ones that can stop your
application from starting.

---

## 1. `Registry` is gone

`Registry` and the global registry validation pass were removed and replaced by
`ProviderExpansion`, a four-step breadth-first walk of the declared graph. If you imported
it, you will get an `ImportError`:

```python
from dependency.core import Registry   # 1.1.7
```

**What to do instead.** Nothing, in almost every case. `Registry` was internal machinery
that happened to be exported: expansion now happens automatically inside
`Entrypoint.initialize()`, and you never had to call it yourself.

If you were reading it to find out *why* a graph failed, the answer is now a typed result
instead of a lookup. `ExpansionResult` and `ExpansionFailure` are public:

```python
from dependency.core import ExpansionFailure, ExpansionResult
```

Every failure carries the **import chain** that produced it, which is what an error message
looks like now:

```
Provider expansion failed:
  Provider Clock has no implementation (imported via: TemperatureSensor → Clock)
  Provider TemperatureSensor has unresolvable dependency: Clock
```

The internal fallback plugin for orphan providers is also gone. An orphan — a component
declared with no `module=` — is now adopted into the container of whichever provider first
imports it. You do not declare anything for this to happen.

---

## 2. Two behaviours changed

### Bootstrap now runs in dependency order

Previously, which `bootstrap=True` component ran first was **unspecified**: the framework
iterated a `set`. Now a provider's required imports bootstrap before it, and components
that became ready together run in name order.

**Who this affects.** If your application worked around the old arbitrary order — by
sequencing a warm-up call from your entrypoint, for instance — that workaround is probably
now unnecessary. It is also harmless to keep; check it rather than delete it blind.

**Who this breaks.** Code that accidentally depended on the arbitrary order it happened to
get. There is no way to detect this from the outside; if a component's `bootstrap` assumed
another had *not* run yet, it will now find that it has.

To restore the old behaviour, pass a `set` to `ResolutionStrategy.initialize` yourself
instead of the list `resolution` returns. This is not recommended and exists only so the
change is reversible.

### Two providers with the same name now raise

A provider's name is its class name, and the dot-path built from it is the reference
consumers wire against. Two different providers claiming one name under one container used
to **overwrite silently**: the runtime resolved one, and every caller of the other failed
with an error that named neither.

That is now a `DeclarationError` at attach time:

```
Two providers claim the name 'Storage' under the same container: ...
```

**What to do.** Rename one of the classes, or declare them under different modules.
Providers with the same name under *different* containers are unaffected and remain
perfectly legal.

---

## 3. Signature and packaging changes

| What | 1.1.7 | 2.0.0 |
|---|---|---|
| Minimum Python | declared `>=3.11`, could not import on 3.11 | **3.12** |
| `dependency_injector` | unbounded | `>=4.48.2,<5` — 4.48.2 added the `warn_unresolved` wiring argument the framework relies on |
| `graphviz` | imported, never declared | the `[graph]` extra: `pip install module-dependency[graph]` |
| `ResolutionStrategy.injection` | returned `None` | returns the resolution order |
| `ResolutionStrategy.resolution` | returned `set` | returns `list`, in resolution order |
| `InjectionResolver.resolve_providers` | returned `set` | returns `list` |
| `Entrypoint(strategy=...)` | defaulted to `ResolutionStrategy()` | defaults to `None` and builds one per instance — the old default was one object shared by every `Entrypoint` in the process |
| `Container.config` | one `Configuration` shared by every container in the process | per instance |
| `Composite.getChildren()` | method | the `children` property |

The return-type changes are additive in practice: code that ignored the return value is
unaffected, and code that iterated it still iterates.

`Container.config` is the one to look at if you build more than one container in a process
— for example in tests. Configuration used to leak between them; it no longer does.

---

## 4. What is new and optional

### The `dependency` command

```bash
pip install module-dependency
dependency check myapp.plugins:PLUGINS --import myapp.imports
```

`check` expands and resolves your graph **without wiring or bootstrapping it**, so it is
safe in CI, and it prints the same import chains a failed startup would. `show` prints the
injection tree with each bound implementation; `graph` renders it to SVG with the `[graph]`
extra; `new plugin|module|component|instance` scaffolds a file.

The `--import` flag matters: implementations register themselves when their module is
imported, so without it `check` sees a graph with nothing in it — and says so rather than
reporting success.

### The pytest plugin

```bash
pip install module-dependency[testing]
```

Registers automatically. `dependency_container` gives a test a fresh `Container`; nothing
is autouse, so installing it changes no existing behaviour.

**Known limitation, stated plainly:** declaration is still a process-global, import-time
side effect with no teardown. The plugin cannot reset it, and the package carries a test
that fails the day that stops being true.

---

## No deprecation path

There is none, and there will not be one. A major release removes; that is what a major
means. This is a decision rather than an omission: promising a deprecation path is a
commitment owed on every removal afterwards.

What you get instead is that a removal can never ship *silently* — the public API is
snapshotted and compared on every build, so a name leaving `dependency.core.__all__`
forces a major version bump before it can be released.

---

## If something still does not start

Run `dependency check` against your own entrypoint. It reports the same diagnostics startup
would, without running your application, and the import chain in the message names both the
provider that is missing and who asked for it.
