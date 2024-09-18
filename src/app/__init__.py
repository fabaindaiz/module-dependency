import time
from src.library.dependencies.loader import Container, resolve_dependency

class AppEnvironment:
    init_time = time.time()
    print("Application starting")

    import src.plugin.providers as plugin
    import src.services.providers as services

    dependencies = [
        *services.get(),
        *plugin.get(),
    ]

    container = Container()
    container.config.from_json("config/main.json")
    resolve_dependency(container, dependencies)

    print(f"Application started in {time.time() - init_time} seconds")