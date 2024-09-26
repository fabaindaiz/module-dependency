import time
from dependency.core import Module, module
from dependency.core.container import Container
from dependency.core.loader import resolve_dependency
from example.plugin import Plugin
from example.services import Services

@module(
    imports=[
        Plugin,
        Services,
    ]
)
class Application(Module):
    pass

class AppEnvironment:
    init_time = time.time()
    print("Application starting")

    container = Container()
    container.config.from_json("src/example/main.json", required=True)

    resolve_dependency(
        container,
        module=Application # type: ignore
    )

    print(f"Application started in {time.time() - init_time} seconds")