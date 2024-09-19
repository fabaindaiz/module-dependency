import time
from core.loader import Container, resolve_dependency

from core import module
from plugin import Plugin
from services import Services

@module(
    imports=[
        Plugin,
        Services,
    ]
)
class Application:
    pass

class AppEnvironment:
    init_time = time.time()
    print("Application starting")

    container = Container()
    container.config.from_json("config/main.json")

    dependencies = Application
    resolve_dependency(container, dependencies)

    print(f"Application started in {time.time() - init_time} seconds")