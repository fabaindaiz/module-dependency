import time
from src.plugin.manager.container import ManagerMixin
from src.app import AppEnvironment

class MainApplication(AppEnvironment, ManagerMixin):
    def loop(self):
        while True:
            time.sleep(1)