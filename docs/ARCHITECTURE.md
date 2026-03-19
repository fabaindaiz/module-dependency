# Architecture — module-dependency

## Overview

`module-dependency` is a dependency injection framework for modular Python applications,
built on top of [`dependency-injector`](https://python-dependency-injector.ets-labs.org/).
It adds a structured layer of abstraction that enforces modular design through a hierarchy
of organizational and providable units, with a resolution process that validates and wires
the full dependency graph before the application starts.

The framework is designed with embedded and long-running applications in mind: all
dependencies are declared statically, resolved eagerly at startup, and injected
transparently at runtime.

---

## Mental Model

The framework organizes an application around two orthogonal concepts:

- **Structure**: how code is organized and grouped (Plugin, Module)
- **Providers**: how dependencies are declared and injected (Component, Instance, Product)

Every class in the framework is either a structural container or a providable unit,
and the two hierarchies mirror each other at runtime through the injection tree.

---

## Core Concepts

### Plugin

A `Plugin` is the top-level structural unit. It represents a self-contained, reusable
feature of the application. Plugins are the entry points into the dependency graph — only
classes registered under a plugin (directly or through child modules) will be resolved
at startup.

Plugins can declare a typed `config` attribute (a Pydantic `BaseModel`), which is
automatically populated from the application `Container` during resolution.

```python
@module()
class HardwarePlugin(Plugin):
    meta = PluginMeta(name="HardwarePlugin", version="0.1.0")
    config: HardwarePluginConfig  # populated from Container on resolution
```

Plugins have no parent module — they are roots of the injection tree.

### Module

A `Module` groups related components under a plugin. Modules can be nested to represent
sub-features or layers within a plugin. They carry no logic themselves; their only role
is structural — to define scope and namespace within the injection tree.

```python
@module(module=HardwarePlugin)
class HardwareFactoryModule(Module):
    pass
```

### Component

A `Component` declares an interface (or contract) for a dependency. It is the unit that
consumers depend on — other classes declare `Component` types in their `imports`, and
the framework ensures a concrete implementation is available before they run.

A component without a declared `provider` is purely an interface declaration: it can
be depended upon, but cannot be provided directly until an `Instance` implements it.

```python
@component(module=HardwarePlugin)
class HardwareFactory(ABC, Component):
    @abstractmethod
    def createHardware(self, product: str) -> Hardware: ...
```

### Instance

An `Instance` is the concrete implementation of a `Component`. It inherits from the
component class and registers itself as the provider for that interface. Multiple
instances can be declared for the same component — the last one registered wins
(with a warning log).

```python
@instance(
    imports=[HardwareObserver, HardwareA, HardwareB],
    provider=providers.Singleton,
)
class HardwareFactoryCreatorA(HardwareFactory):
    def __init__(self):
        self.__factory = HardwareFactory.provide()
```

### Product

A `Product` is functionally identical to a `Component` with `provider=providers.Factory`.
The distinction is semantic: Products represent objects that are instantiated on demand
(not managed as singletons), typically by a factory or service that creates them as
part of its operation.

```python
@product(
    imports=[NumberService],
    provider=providers.Factory,
)
class HardwareA(Hardware, Product):
    @inject
    def doStuff(self, operation: str, number: NumberService = LazyProvide[NumberService.reference]):
        ...
```

Products are declared as dependencies of the instances or other products that create
them — not consumed directly by end users of the framework.

---

## Injection Hierarchy

The structural and injection trees are parallel. At the structural level:

```
Entrypoint
└── Plugin (root container)
    └── Module (child container)
        ├── Component / Instance (provider)
        └── Product (provider)
```

At the injection level, this maps to a tree of `ContainerInjection` and
`ProviderInjection` objects:

```
ContainerInjection (Plugin)
└── ContainerInjection (Module)
    ├── ProviderInjection (Component)
    └── ProviderInjection (Product)
```

Each node in this tree knows its parent, and the full dot-separated path from root to
node is used as the `reference` string for `dependency-injector`'s wiring system
(e.g. `HardwarePlugin.HardwareFactory`).

---

## Resolution Process

Resolution happens in five sequential phases, triggered by `Entrypoint.initialize()`:

### Phase 1 — Module Resolution (`resolve_modules`)

Each plugin's `ContainerInjection` tree is attached to the application `Container`.
Plugin configuration is validated and populated from the container config at this point.
This phase sets up the structural scaffolding before any providers are touched.

### Phase 2 — Injectable Collection (`resolve_injectables`)

Each plugin walks its injection tree and yields the `Injectable` objects for all
providers that have a valid implementation. Providers without implementation are silently
skipped (or warned, depending on `strict_resolution`).

### Phase 3 — Graph Expansion (`expand`)

Starting from the collected injectables, the resolver follows each provider's `imports`
recursively to discover the full transitive dependency graph. Providers marked with
`partial_resolution=True` are included in the set but their imports are not followed —
this is the escape hatch for providers that depend on external or optional components.

### Phase 4 — Topological Resolution (`injection`)

Dependencies are resolved in layers. In each iteration, all providers whose imports are
already resolved are marked as resolved. If an iteration produces no new resolved
providers, resolution has deadlocked — the error handler checks for circular dependencies
first, then reports missing implementations.

```
Layer 1: providers with no imports → resolved
Layer 2: providers whose imports are all in Layer 1 → resolved
...
```

### Phase 5 — Wiring and Initialization

After all providers are resolved, their modules are wired into the `Container` using
`dependency-injector`'s wiring mechanism. Then, providers with `bootstrap=True` have
their implementation instantiated eagerly, triggering any `__init__` logic. If `__init__`
raises `CancelInitialization`, the bootstrap is skipped with a warning rather than
crashing the application.

---

## The Registry

The `Registry` is a global class-level store of all `ContainerInjection` and
`ProviderInjection` objects ever created. It is populated at decoration time (when
`@module`, `@component`, etc. are applied), before any resolution happens.

Its current role is diagnostic: `Registry.validation()` runs before resolution and
warns about any containers or providers that have no parent module (i.e., were declared
without being registered under any plugin or module). These are called "orphan"
providers, and the `FallbackPlugin` handles them at initialization time.

---

## Dependency Injection at Runtime

Once resolved, dependencies can be accessed in two ways:

**Direct provision** — call `.provide()` on the component class. This returns the
underlying `dependency-injector` provider result (a singleton instance, a new factory
instance, etc.):

```python
factory: HardwareFactory = HardwareFactory.provide()
```

**`@inject` with `LazyProvide`** — for method-level injection, use the `@inject`
decorator from `dependency-injector` combined with `LazyProvide`. The `Lazy` prefix
is required to defer the reference resolution to runtime rather than import time:

```python
@inject
def doStuff(self,
    operation: str,
    number: NumberService = LazyProvide[NumberService.reference],
) -> None:
    ...
```

`LazyProvide`, `LazyProvider`, and `LazyClosing` mirror the standard `Provide`,
`Provider`, and `Closing` markers from `dependency-injector`, but accept either a
callable returning a reference string, or a `ProviderMixin` class directly (which
internally calls `.reference` on it).

---

## Provider Types

The framework supports the three provider types from `dependency-injector`:

| Type | Behavior | Typical use |
|---|---|---|
| `providers.Singleton` | One instance for the lifetime of the container | Services, observers, factories |
| `providers.Factory` | New instance on every `.provide()` call | Products, short-lived objects |
| `providers.Resource` | Singleton with context manager lifecycle (`__enter__`/`__exit__`) | Resources that need explicit cleanup |

---

## Entrypoint

The `Entrypoint` class orchestrates the full startup sequence. The expected pattern is:

```python
class MyApplication(Entrypoint):
    def __init__(self) -> None:
        container = Container.from_dict(config={...})
        super().__init__(container, PLUGINS)

        # Import all instance modules here — this triggers @instance decoration,
        # which registers implementations into the injection tree.
        import my_app.imports

        # Run the five-phase resolution process.
        super().initialize()
```

The separation between `__init__` and `initialize()` is intentional: instance imports
must happen after the structural tree is set up (after `super().__init__`), but before
resolution starts (before `super().initialize()`).

---

## Imports File Convention

Because `@instance` and `@product` decorators register themselves at import time,
implementations must be imported before `initialize()` is called. The convention is
to collect all these imports in a dedicated `imports.py` file per plugin:

```python
# example/plugin/hardware/imports.py
import example.plugin.hardware.bridge.bridgeA
import example.plugin.hardware.factory.providers.creatorA
import example.plugin.hardware.observer.publisherA
```

And then import all plugin imports files from the application's root `imports.py`:

```python
# app/main/imports.py
import example.plugin.base.imports
import example.plugin.hardware.imports
import example.plugin.reporter.imports
```

This pattern makes the set of active implementations explicit and easy to swap — for
example, to run in a test environment with fake implementations, you would create an
alternative imports file that imports the fakes instead.

---

## Fallback Plugin

Providers that are declared without a parent module (orphan providers) would fail
resolution because they have no `ContainerInjection` to attach to, and therefore no
`reference` string for wiring. The `FallbackPlugin` is an internal plugin created
at initialization time that adopts all such orphan providers, attaches them to its
container, and marks them with `strict_resolution=False` so they do not block
resolution if they lack an implementation.

This is a safety mechanism, not a recommended pattern. Orphan providers are warned
about in `Registry.validation()` and should be assigned to a proper module.

---

## Error Handling

| Exception | When raised |
|---|---|
| `DeclarationError` | A provider is accessed (`.provide()`, `.reference`) before being resolved, or has no implementation |
| `ResolutionError` | The topological resolution deadlocks (circular dependency or unresolved import) |
| `ProvisionError` | Plugin config validation fails, or a provider without a parent tries to build a reference |
| `InitializationError` | A bootstrapped provider's `__init__` raises an unexpected exception |
| `CancelInitialization` | Raised intentionally inside `__init__` to skip bootstrap without crashing |

---

## Internal Class Map

```
dependency.core
├── agrupation
│   ├── Entrypoint          — application startup orchestrator
│   ├── Plugin              — root structural unit, carries config
│   ├── Module              — intermediate structural grouping
│   └── FallbackPlugin      — internal, adopts orphan providers
├── declaration
│   ├── Component           — interface declaration + ProviderMixin base
│   ├── Instance            — concrete implementation of a Component
│   └── Product             — Component alias, Factory default, legacy support
├── injection
│   ├── Injectable          — tracks implementation, imports, resolution state
│   ├── ContainerInjection  — injection node for structural units (Module/Plugin)
│   ├── ProviderInjection   — injection node for providable units (Component/Product)
│   ├── ContainerMixin      — class-level methods for structural units
│   ├── ProviderMixin       — class-level methods for providable units
│   └── LazyProvide/Provider/Closing — deferred wiring markers
└── resolution
    ├── Container           — DynamicContainer with config helpers
    ├── Registry            — global store of all injection nodes
    ├── InjectionResolver   — orchestrates the five resolution phases
    └── ResolutionStrategy  — implements expand, injection, wiring, initialize
```
