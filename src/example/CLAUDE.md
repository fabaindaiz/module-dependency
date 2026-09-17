# example/ — a monitoring station

Not packaged (`[tool.hatch.build.targets.wheel].packages` is `src/dependency` only), but
it is the primary teaching artefact and the only thing that exercises the full startup
path end to end. `tests/example/` is its regression guard: **if a core API changes, this
breaks there before it breaks for a reader.**

A sensor station: it samples probes on a cadence, stores the readings, raises alerts when
a threshold is crossed, and shows them on a panel — if the unit has one.

```
app/main/          MonitoringStation(Entrypoint), plugins.py, imports.py
plugin/
  runtime/         Clock, DeferredService, StationState — depends on nothing
  sensors/         probes, SensorGroup, Sampler
  storage/         ReadingStore (memory or jsonl)
  telemetry/       events, StationObserver, AlertSink
  display/         StatusPanel — OPTIONAL, the point of the example
config.json        one file, one section per plugin
```

Run it: `hatch run build:example` (Ctrl-C to stop).

## What each piece demonstrates

| Feature | Where | Why it is there |
|---|---|---|
| **`optional=`** | `telemetry/alerts/console.py` | The differentiator. `StatusPanel` is optional, so a unit with no screen starts anyway |
| `imports.py` swap | `storage/imports.py`, `runtime/clock/` | One line decides memory vs disk, real clock vs manual |
| Typed per-plugin config | every `settings.py` | Each plugin validates the same root dict and sees only its own section |
| `bootstrap=True` | `runtime/deferred`, `sensors/sampler`, `telemetry/alerts` | Things that must exist before anything asks for them |
| `providers.Resource` | `storage/store/jsonl.py` | The only provider with a lifecycle: `__enter__` / `__exit__` |
| `CancelInitialization` | `sensors/probes/pressure.py` | Hardware that is not fitted declines to start without failing the graph |
| Library contracts | `telemetry/observer`, `sensors/group`, `runtime/state` | `ObserverComponent`, `CompositeComponent`, `StateComponent` |
| A plain ABC vs a component | `sensors/interfaces.py` vs `sensors/probes/` | `SensorReader` is an ABC because a station has several probes; a component has exactly one implementation |

## Two framework limits this app has to work around

Both measured. Do not "simplify" the code that handles them.

- **Bootstrap order is unspecified** (D-035). `ResolutionStrategy.initialize` iterates a
  `set`, so a `bootstrap=True` component cannot assume another has run. That is why the
  sampler's warm-up is **not** in its `__init__`: it is sequenced from
  `MonitoringStation.__init__`, after `initialize()`, when every subscriber is registered.
- **The root `Container` cannot see plugin providers** (D-034). Its own `.providers` is
  just `['__self__']` because providers live in nested sub-containers. So
  `container.shutdown_resources()` is a no-op and `init_resources()` initialises nothing.
  `MonitoringStation.stop()` walks the injection tree and shuts down each `Resource`
  itself.

## Anatomy of a plugin

```
plugin/<name>/
  __init__.py      @module() class <Name>Plugin(Plugin) — meta + typed config
  settings.py      the pydantic models: a <Name>Settings and a <Name>Config view
  interfaces.py    plain ABCs and dataclasses — the vocabulary, no decorators
  imports.py       imports every implementation module, then re-exports the Plugin
  <feature>/       __init__.py declares the @component; siblings hold the @instance
```

Copy `plugin/sensors/` for a new plugin: it is the only one with every piece — several
components over one ABC, a composite, a bootstrapped service, and a cancelled one.

## Config

One `config.json`, one section per plugin. Each plugin's `Config` model is a *view*:

```python
class SensorsSettings(BaseModel):  # the actual fields
    sample_interval_s: float = 1.0


class SensorsConfig(BaseModel):  # the view onto the root document
    sensors: SensorsSettings = SensorsSettings()
```

Every plugin validates the same root dictionary; pydantic ignores keys it does not know,
so one file serves all of them without a plugin's settings leaking into another's model.

The path is resolved against the package, not the working directory — a unit started by
systemd from `/` has to find its config.

## The `imports.py` convention

`@instance` and `@product` register themselves **at import time**. Nothing that is not
imported before `initialize()` exists. Import **modules**, never individual functions:
`dependency-injector` cannot patch an individually imported function and the injection
silently does not happen.

`app/main/imports.py` is therefore the real configuration of which implementation wins.

## `Entrypoint.__init__` vs `initialize()`

The order in `app/main/__init__.py` is load-bearing:

1. `super().__init__(container, PLUGINS)` — structural tree, plugin configs resolved.
2. `import example.app.main.imports` — implementations register themselves.
3. `super().initialize()` — expansion, wiring, bootstrap.
4. *then* anything that must run after the whole graph is up, like `sampler.warmup()`.

Moving the import to the top of the file breaks startup in a way the error will not
explain.

## Reusing a library contract

When `dependency.library.components` has a contract, declare from it rather than
rewriting the interface. `telemetry/observer/` is the worked case:

```python
@component(module=TelemetryPlugin)
class StationObserver(ObserverComponent[StationEvent]):
    pass


@instance(imports=[DeferredService], provider=providers.Singleton)
class DeferredStationObserver(EventPublisherMixin[StationEvent], StationObserver):
    def update(self, context: StationEvent) -> None:
        self.__deferred.create_task(self.publish(context))
```

Parameterise the contract with this domain's own type (D-031), and put the mixin **first**
so its `__init__` runs. What stays here and never moves into the library: the `module=`,
the `provider=`, the `imports=`, and the domain types. See D-030.

## Local conventions

- `print()` in the panel, `logging` everywhere else. The panel stands in for a screen.
- `snake_case` throughout, matching the framework. The old example used `camelCase`; the
  rewrite dropped it, so D-021 no longer has a subject.
