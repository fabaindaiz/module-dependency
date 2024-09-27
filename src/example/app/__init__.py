import time
from dependency.core import Module, module
from dependency.core.container import Container
from dependency.core.loader import resolve_dependency
from example.module import Plugin

@module(
    imports=[
        Plugin
    ]
)
class Application(Module):
    pass

class AppEnvironment:
    init_time = time.time()
    print("Application starting")

    container = Container.from_json("src/example/main.json", required=True)
    resolve_dependency(container, appmodule=Application)

    print(f"Application started in {time.time() - init_time} seconds")