import time
import logging
from dependency.core import Entrypoint, Container

logger = logging.getLogger("root")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class MainApplication(Entrypoint):
    def __init__(self) -> None:
        # Import all the instances that will be used on the application
        # You can also import the plugins list from the imports file
        from example.app.main.imports import PLUGINS
        
        container = Container.from_dict(config={"config": True}, required=True)
        super().__init__(container, PLUGINS)

    def main_loop(self) -> None:
        while True:
            time.sleep(1)