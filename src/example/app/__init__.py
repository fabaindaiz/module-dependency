import time
import logging
from dependency.core.container import Container
from dependency.core.loader import resolve_dependency
from example.module import MainModule
logger = logging.getLogger("root")

class MainApplication:
    def __init__(self) -> None:
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())

        init_time = time.time()
        logger.info("Application starting")

        container = Container.from_json("src/example/main.json", required=True)
        resolve_dependency(container, appmodule=MainModule)

        logger.info(f"Application started in {time.time() - init_time} seconds")

    def loop(self) -> None:
        while True:
            time.sleep(1)