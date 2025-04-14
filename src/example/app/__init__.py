import logging
import time
from dependency.core.container import Container
from dependency.core.loader import resolve_dependency
from example.app.module import MainModule

class MainApplication:
    init_time = time.time()
    logger = logging.getLogger("root")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    def __init__(self) -> None:
        container = Container.from_dict(config={"config": True}, required=True)
        resolve_dependency(container, appmodule=MainModule) # type: ignore
        self.logger.info(f"Application started in {time.time() - self.init_time} seconds")

    def loop(self) -> None:
        while True:
            time.sleep(1)