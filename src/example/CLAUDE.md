# example/ — executable documentation

Not packaged (`[tool.hatch.build.targets.wheel].packages` is `src/dependency` only), but
it is the primary teaching artefact and the only place that exercises the full startup
path end to end. `hatch run build:example` is part of the verification story for
`core/resolution/` — unit tests reach that path only in pieces.

**If a core API changes, this breaks first.** That is the point. Keep it compiling.

## Anatomy of a plugin

```
plugin/<name>/
  __init__.py      @module() class <Name>Plugin(Plugin) — meta + typed config
  settings.py      the pydantic BaseModel named in the config type hint
  interfaces.py    plain ABCs, no decorators — the vocabulary of the plugin
  imports.py       imports every implementation module, then re-exports the Plugin
  <feature>/       __init__.py declares the @component; siblings hold @instance
```

Copy `plugin/hardware/` for a new plugin. It is the only one that shows every piece:
a factory component, products with `@inject`, an observer, and a bridge.

## The `imports.py` convention

`@instance` and `@product` register themselves at **import time**. Nothing that is not
imported before `initialize()` exists. So each plugin collects its implementation
imports in `imports.py`, and `app/main/imports.py` imports those.

Import **modules**, never individual functions — `dependency-injector` cannot patch an
individually imported function, and the injection silently does not happen.

Swapping implementations (fakes for tests, a different backend) is done by writing an
alternative `imports.py`, not by editing declarations. `plugin/base/number/fake.py` is
the example.

## `Entrypoint.__init__` vs `initialize()`

The split is load-bearing and `app/main/__init__.py` shows the order:

1. `super().__init__(container, PLUGINS)` — structural tree, plugin configs resolved.
2. `import example.app.main.imports` — implementations register themselves.
3. `super().initialize()` — expansion, wiring, bootstrap.

Implementations must be imported *after* step 1 and *before* step 3. Moving the import
to the top of the file breaks startup in a way the error message will not explain.

## Reusing a library contract

When `dependency.library.components` already has a contract, declare from it instead of
rewriting the interface. `plugin/hardware/observer/` is the worked case:

```python
@component(module=HardwarePlugin)
class HardwareObserver(ObserverComponent[HardwareEventContext]):
    pass                                      # contract from the library

@instance(imports=[DeferredService], provider=providers.Singleton)
class HardwareObserverA(EventPublisherMixin[HardwareEventContext], HardwareObserver):
    def update(self, context: HardwareEventContext) -> None:
        self.__deferred.run(self.publish(context))   # only the dispatch policy
```

Parameterise the contract with this domain's `EventContext` subclass — that is what lets
`update` be typed to the domain without breaking Liskov (D-031). Put the mixin **first** in
the bases so its `__init__` runs.

What stays here and never moves into the library: the `module=`, the `provider=`, the
`imports=`, and the domain types. See D-030 for why the library ships nothing decorated.

## Local conventions that differ from `src/dependency/`

- Methods here are `camelCase` (`createHardware`, `getRandomNumber`) while the framework
  is `snake_case`. This is the example's public surface; it is **not** being changed
  (D-021). Do not "fix" it, and do not copy it into `src/dependency/`.
- `print()` is used instead of logging, deliberately — it is what makes the example
  readable when run.
- `LazyProvide[X]` (subscript) and `LazyProvide(X)` (call) are equivalent; `_Marker`
  implements `__class_getitem__`. The docs use both. Prefer the subscript form here,
  matching `factory/products/productA.py`.
