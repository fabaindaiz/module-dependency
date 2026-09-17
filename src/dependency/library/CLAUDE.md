# library/ — batteries for applications built on the framework

Part of the product, but not the core. These are prebuilt pieces an application using
`dependency` will want. `src/example/` uses them, which is how they get exercised.

## The rule: nothing here is decorated

**No `@component`, `@instance`, `@product` or `@module` may appear in `library/`.**
Enforced in `audit_dependency.py::check_library_undecorated`.

Declaration is a global import-time side effect, `injection` is a class attribute with one
instance per process, and `Injectable.set_implementation` is **last-wins**. A component
declared by a library would therefore make the active implementation depend on **import
order**, not on intent — measured, D-030. It would also become public API forever (D-013).

So the application applies the decorators, and keeps the `module=`, the `provider=`, the
`imports=` and its own domain types.

## The three layers

| Layer | What it is | Where |
|---|---|---|
| **Primitives** | Plain classes, useful even outside the framework | `patterns/` — `EventPublisher`, `Composite`, `StateHolder` |
| **Contracts** | Undecorated `Component` subclasses: the reusable interface | `components/` — `ObserverComponent` |
| **Mixins** | The implementation body, composed onto a contract | `components/` — `EventPublisherMixin` |

Copy `components/observer.py` for a new contract. It shows the whole shape:

```python
CONTEXT = TypeVar("CONTEXT", bound=EventContext)


class ObserverComponent(Component, Generic[CONTEXT]):  # no decorator
    @abstractmethod
    def update(self, context: CONTEXT) -> None: ...


class EventPublisherMixin(Generic[CONTEXT]):  # the body
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._publisher = EventPublisher()
```

**Contracts must be `Generic` in their domain type** (D-031). Without it, an application
narrowing the parameter — `update(self, context: HardwareEventContext)` — violates Liskov
and `mypy --strict` rejects it. A contract that cannot be specialised will not be used.

Leave out of the mixin anything that is a *policy* rather than *plumbing*. `EventPublisherMixin`
deliberately does not implement `update`: publishing is a coroutine, and whether it is
awaited, scheduled on a task loop or run in a thread pool is an application decision. See
`src/example/plugin/hardware/observer/publisherA.py`, which drives it through
`DeferredService`.

## Dependency direction

`library` imports from `core`; **`core` never imports from `library`** (D-019). That cycle
was closed when `handle_exit` moved to `core/utils/threading.py`; `library/threading.py`
re-exports it so the old import path still works.

## Optional dependencies

`patterns/`, `components/` and `threading.py` use only the standard library and the
framework. **`graph/` requires `graphviz`, which is an extra**:

```bash
pip install module-dependency[graph]
```

Any module here needing a package outside `[project.dependencies]` must declare it in
`[project.optional-dependencies]` and fail with a message naming the extra, not with a bare
`ModuleNotFoundError`. Enforced in `audit_dependency.py::check_declared_imports`.

## Test coverage here is 23%

`graph/` has no tests at all. The `NameError` that broke it on every supported Python
shipped through that gap. See the roadmap.
