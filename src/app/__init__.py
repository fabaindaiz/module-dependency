import time
from core.loader import Container, resolve_dependency

class AppEnvironment:
    init_time = time.time()
    print("Application starting")

    import plugin.providers as plugin
    import services.providers as services

    dependencies = [
        *services.get(),
        *plugin.get(),
    ]

    container = Container()
    container.config.from_json("config/main.json")
    resolve_dependency(container, dependencies)

    print(f"Application started in {time.time() - init_time} seconds")