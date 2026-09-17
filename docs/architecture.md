# Architecture — module-dependency

`module-dependency` is a dependency injection framework for modular Python applications,
built on [`dependency-injector`](https://python-dependency-injector.ets-labs.org/). It adds
a structured layer that enforces modular design through a hierarchy of organisational and
providable units, and validates the full dependency graph before the application starts.

The framework targets embedded and long-running applications: dependencies are declared
statically, resolved eagerly at startup, and injected transparently at runtime.

**The invariant everything serves:** the entire dependency graph is validated before the
first user object is constructed. If it cannot be satisfied, the application does not
start, and the error names the offending provider and its import chain. See `decisions.md`
D-001.

---

## Mental model

Two orthogonal concepts:

- **Structure** — how code is organised and grouped: `Plugin`, `Module`.
- **Providers** — how dependencies are declared and injected: `Component`, `Instance`,
  `Product`.

Every class is either a structural container or a providable unit, and the two hierarchies
mirror each other at runtime through the injection tree.

---

## Core concepts

### Plugin

The top-level structural unit: a self-contained, reusable feature. Plugins are the roots
of the dependency graph — only classes registered under a plugin (directly or through
child modules) are resolved at startup. They have no parent module.

A plugin may declare a typed `config` attribute (a pydantic `BaseModel`). It is populated
from the application `Container` during resolution, via `get_type_hints`.

```python
@module()
class HardwarePlugin(Plugin):
    meta = PluginMeta(name="HardwarePlugin", version="0.1.0")
    config: HardwarePluginConfig   # a type hint, not a method
```

### Module

Groups related components under a plugin, and may nest. Carries no logic; its only role is
to define scope and namespace within the injection tree.

```python
@module(module=HardwarePlugin)
class HardwareFactoryModule(Module):
    pass
```

### Component

Declares an interface. Other classes name `Component` types in their `imports`, and the
framework guarantees a concrete implementation exists before they run. A component with no
`provider=` is a pure interface declaration: it can be depended upon, but nothing can be
provided until an `Instance` implements it.

```python
@component(module=HardwarePlugin)
class HardwareFactory(Component):
    @abstractmethod
    def createHardware(self, product: str) -> Hardware: ...
```

### Instance

The concrete implementation of a `Component`. It inherits from the component class and
takes ownership of its `Injectable`. If a second `@instance` targets the same component,
the last one registered wins and a warning is logged.

```python
@instance(
    imports=[HardwareObserver, HardwareA, HardwareB],
    provider=providers.Singleton,
)
class HardwareFactoryCreatorA(HardwareFactory):
    def __init__(self) -> None:
        self.__observer: HardwareObserver = HardwareObserver.provide()
```

### Product

Functionally a `Component` with `providers.Factory` as the default. The distinction is
semantic: products are instantiated on demand, typically by a factory or service, rather
than consumed directly as long-lived services.

```python
@product(module=HardwarePlugin, imports=[NumberService], provider=providers.Factory)
class HardwareA(Hardware, Product):
    @inject
    def doStuff(self, operation: str,
                number: NumberService = LazyProvide[NumberService.reference]) -> None:
        ...
```

`LazyProvide[X]` and `LazyProvide(X)` are equivalent — `_Marker` implements
`__class_getitem__`.

---

## Injection hierarchy

The structural and injection trees are parallel:

```
Entrypoint                          ContainerInjection (Plugin)
└── Plugin (root container)         └── ContainerInjection (Module)
    └── Module (child container)        ├── ProviderInjection (Component)
        ├── Component / Instance        └── ProviderInjection (Product)
        └── Product
```

Each node knows its parent, and the dot-separated path from root to node is the
`reference` string `dependency-injector` wires against (e.g. `HardwarePlugin.HardwareFactory`).

**A `reference` is a contract.** Renaming a class or moving it between modules changes it.
Two providers with the same class name under one container collide: the second silently
overwrites the first via `setattr`. See D-020.

---

## Resolution

Triggered by `Entrypoint.initialize()`. Three stages, and the middle one is where the work
happens.

### Stage 1 — Module resolution (`resolve_modules`)

Each plugin's `ContainerInjection` tree is attached to the application `Container`, and
plugin configuration is validated and populated. Structural scaffolding only; no providers
are touched.

### Stage 2 — Expansion (`ProviderExpansion.expand`)

A breadth-first walk in four steps. The class docstring in
`core/resolution/expansion.py` is the authoritative version of this list.

1. **Seed** — implemented providers from the structural tree, plus any `extra`.
2. **Expansion** — BFS through `imports` and `optional_imports`, discovering undeclared
   providers. Each undeclared provider is adopted into the container of whichever provider
   first imported it.
3. **Conditions** applied while walking:

   | Import kind | Implementation | `strict_resolution` | Result |
   |---|---|---|---|
   | required | missing | `True` | `ExpansionFailure` |
   | required | missing | `False` | skipped, warned |
   | optional | missing | any | skipped silently, never a failure |

4. **Cascade** — a provider with a failed **required** import also fails, transitively.
   Optional failures never cascade.

The result is an `ExpansionResult` carrying both `resolved` and `failures`.
`raise_if_failed()` raises `ResolutionError` with the full import chain for each failure
(`A → B → C`), which is the diagnostic the whole design depends on (D-006).

### Stage 3 — Injection, wiring, initialisation (`ResolutionStrategy.resolution`)

- **`injection`** resolves layer by layer: each pass marks every provider whose imports are
  already resolved. A pass that resolves nothing means deadlock — `raise_resolution_error`
  then checks for circular dependencies first, and reports unresolved imports second.
- **`wiring`** calls `container.wire(modules=..., warn_unresolved=True)` per provider, then
  `check_dependencies()` and `init_resources()` if `ResolutionConfig.init_container`.

  Note: `check_dependencies()` validates **nothing** in this framework — it only inspects
  `providers.Dependency`, which `validation._PROVIDERS` makes impossible to construct.
  Measured: zero such providers in the example app. See D-005.
- **`initialize`** runs the `bootstrap` callable of every provider declared with
  `bootstrap=True`. `CancelInitialization` skips one with a warning; any other exception
  becomes `InitializationError`.

---

## Dependency injection at runtime

**Direct provision** — call `.provide()` on the component class:

```python
factory: HardwareFactory = HardwareFactory.provide()
```

It raises `DeclarationError` if the provider was not resolved. This is the mechanism that
turns what would be a Service Locator runtime failure into a startup failure — see D-011
and the Seemann entry in `references.md`.

**`@inject` with `LazyProvide`** — for method-level injection:

```python
@inject
def doStuff(self, operation: str,
            number: NumberService = LazyProvide[NumberService.reference]) -> None:
    ...
```

`LazyProvide`, `LazyProvider` and `LazyClosing` mirror `dependency-injector`'s `Provide`,
`Provider` and `Closing`, but accept either a callable returning a reference string or a
`ProviderMixin` class directly. The `Lazy` prefix is the point: the reference resolves at
injection time, not import time, when the tree does not yet exist.

---

## Provider types

| Type | Behaviour | Typical use |
|---|---|---|
| `providers.Singleton` | one instance for the container's lifetime | services, observers, factories |
| `providers.Factory` | a new instance per `.provide()` | products, short-lived objects |
| `providers.Resource` | singleton with a context-manager lifecycle | resources needing explicit cleanup |

These three are the **only** permitted types (`validation._PROVIDERS`). Anything else makes
the graph unvalidatable at startup — D-004.

---

## Entrypoint and the import order

```python
class MyApplication(Entrypoint):
    def __init__(self) -> None:
        container = Container.from_dict(config={...}, required=True)
        super().__init__(container, PLUGINS)   # 1. structural tree + plugin configs

        import my_app.imports                  # 2. @instance decorators register

        super().initialize()                   # 3. expansion, wiring, bootstrap
```

The split between `__init__` and `initialize()` is load-bearing. Implementations register
themselves **at import time**, so they must be imported after the structural tree exists
and before resolution starts. Moving the import to the top of the file breaks startup in a
way the error message will not explain.

### The `imports.py` convention

Each plugin collects its implementation imports in `imports.py`, and the application's root
`imports.py` imports those:

```python
# example/plugin/hardware/imports.py
import example.plugin.hardware.bridge.bridgeA
import example.plugin.hardware.factory.providers.creatorA
import example.plugin.hardware.observer.publisherA
```

Import **modules**, never individual functions — `dependency-injector` cannot patch an
individually imported function and the injection silently does not happen (D-008).

This makes the active implementation set explicit and swappable: a test environment uses an
alternative `imports.py` that imports fakes.

---

## Orphan providers

A provider declared without `module=` has no `ContainerInjection` and therefore no
`reference`. During expansion, `_adopt_if_orphan` places it in the container of whichever
provider first imported it. If nothing imports it and it is not a root, expansion fails
with a message telling you to declare it with `module=` or add it via `provides=`.

This is a convenience, not a recommended pattern — declare the module.

---

## Error handling

| Exception | When raised |
|---|---|
| `DeclarationError` | a provider is used before resolution, or has no implementation assigned |
| `ResolutionError` | expansion failed, or topological resolution deadlocked (cycle or unresolved import) |
| `ProvisionError` | plugin config validation failed, or a provider without a parent tried to build a `reference` |
| `InitializationError` | a bootstrapped provider raised an unexpected exception |
| `CancelInitialization` | raised deliberately inside `__init__` to skip bootstrap without crashing |

All inherit from `DependencyError`.

---

## Where a new file goes

| You are adding… | It belongs in |
|---|---|
| a new decorator or declaration rule | `core/declaration/` |
| a new structural unit | `core/agrupation/` |
| tree, binding or wiring-marker logic | `core/injection/` |
| expansion, ordering, diagnostics | `core/resolution/` |
| a generic algorithm with no framework types | `core/utils/` |
| a reusable piece for applications *using* the framework | `library/` |
| a code generator or template | `cli/` |

The allowed dependency direction between these, and the two accepted cycles, are in
`src/dependency/core/CLAUDE.md` and enforced by `tools/audit_dependency.py::check_layering`.

---

## Internal class map

```
dependency.core
├── agrupation
│   ├── Entrypoint          — startup orchestrator
│   ├── Plugin              — root structural unit, carries typed config
│   └── Module              — intermediate structural grouping
├── declaration
│   ├── Component           — interface declaration
│   ├── Product             — Component with a Factory default
│   └── @component/@instance/@product + provider validation
├── injection
│   ├── Injectable          — the interface → implementation binding
│   ├── ContainerInjection  — tree node for structural units
│   ├── ProviderInjection   — tree node for providable units, holds the dep graph
│   ├── ContainerMixin      — class-level API for structural units
│   ├── ProviderMixin       — class-level API for providable units
│   └── LazyProvide/Provider/Closing — deferred wiring markers
├── resolution
│   ├── Container           — DynamicContainer with config helpers
│   ├── ProviderExpansion   — the four-step BFS; ExpansionResult / ExpansionFailure
│   ├── InjectionResolver   — orchestrates the three stages
│   └── ResolutionStrategy  — injection, wiring, initialize
└── utils
    └── find_cycles         — cycle detection for diagnostics
```
