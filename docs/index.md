# module-dependency

A dependency injection framework for modular, long-running Python applications.

Declare components with interfaces, provide implementations of them, and group them into
plugins. The framework resolves and validates the whole dependency graph **before the
application starts** — if it cannot be satisfied, you get a startup error naming the
provider and its import chain, not an `AttributeError` hours later.

```bash
pip install module-dependency
pip install module-dependency[graph]   # adds dependency-graph rendering (needs graphviz)
```

Requires Python 3.12 or newer.

## Where to go

| | |
|---|---|
| **[Architecture](architecture.md)** | the concepts, the resolution process, where a new file goes |
| **[Core reference](reference/core.md)** | generated API documentation |
| **[Decisions](decisions.md)** | every settled question, numbered, with what enforces it |
| **[References](references.md)** | the external sources that changed a decision, and what we do differently |
| **[Roadmap](roadmap.md)** | what is planned and what it collides with |
| **[Full README](https://github.com/fabaindaiz/module-dependency#readme)** | the tutorial-style introduction with complete examples |

## The five minute version

```python
from dependency.core import (
    Component, Container, Entrypoint, Plugin, PluginMeta,
    component, instance, module, providers,
)

@module()
class GreeterPlugin(Plugin):
    meta = PluginMeta(name="GreeterPlugin", version="0.1.0")

@component(module=GreeterPlugin)
class Greeter(Component):
    def greet(self) -> str: ...

@instance(provider=providers.Singleton)
class SpanishGreeter(Greeter):
    def greet(self) -> str:
        return "hola"

class App(Entrypoint):
    def __init__(self) -> None:
        super().__init__(Container.from_dict({"config": True}), [GreeterPlugin])
        super().initialize()

App()
print(Greeter.provide().greet())   # hola
```

Swapping `SpanishGreeter` for another implementation is a change to which module gets
imported, not a change to any declaration. See the `imports.py` convention in
[Architecture](architecture.md).

A plugin without a `config:` type hint logs a warning at startup — harmless, and the
example above omits config to stay short.
