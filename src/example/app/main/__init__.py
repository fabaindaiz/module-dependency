import logging
import time
from dependency.core.injection.container import Container
from dependency.core.agrupation.entrypoint import Entrypoint
from example.plugins.common import CommonPlugin

class MainApplication(Entrypoint):
    init_time = time.time()
    logger = logging.getLogger("root")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    def __init__(self) -> None:
        import example.plugins.common.loader # type: ignore

        container = Container.from_dict(config={"config": True}, required=True)
        super().__init__(container, plugins=[CommonPlugin]) # type: ignore
        self.logger.info(f"Application started in {time.time() - self.init_time} seconds")

    def loop(self) -> None:
        while True:
            time.sleep(1)