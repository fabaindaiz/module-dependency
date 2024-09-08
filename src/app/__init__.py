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

    config = {
        "service1": True,
        "service2": True,
    }

    container = Container()
    container.config.from_dict(config)
    resolve_dependency(container, dependencies)

    print(f"Application started in {time.time() - init_time} seconds")