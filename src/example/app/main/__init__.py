import logging
import time
from dependency.core import Entrypoint, Container
from example.plugin.base import BasePlugin
from example.plugin.hardware import HardwarePlugin
from example.plugin.reporter import ReporterPlugin

PLUGINS = [
    BasePlugin,
    HardwarePlugin,
    ReporterPlugin,
]

class MainApplication(Entrypoint):
    init_time = time.time()
    logger = logging.getLogger("root")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    def __init__(self) -> None:
        import example.app.main.imports
        container = Container.from_dict(config={"config": True}, required=True)
        super().__init__(container, plugins=PLUGINS)
        self.logger.info(f"Application started in {time.time() - self.init_time} seconds")

    def loop(self) -> None:
        while True:
            time.sleep(1)