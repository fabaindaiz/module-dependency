import time
import logging
from src.library.dependencies.loader import Container, resolve_dependency

logger = logging.getLogger("AppEnvironment")

class AppEnvironment:
    init_time = time.time()
    config = {
        "service1": True,
        "service2": True,
    }

    import src.plugin.providers as plugin
    import src.services.providers as services

    dependencies = [
        *services.get(),
        *plugin.get(),
    ]

    container = Container()
    container.config.from_dict(config)
    resolve_dependency(container, dependencies)

    logger.info(f"Application started in {time.time() - init_time} seconds")