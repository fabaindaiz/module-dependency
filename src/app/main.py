from src.plugin.manager.container import ManagerMixin
from src.app import AppEnvironment

class MainApplication(AppEnvironment, ManagerMixin):
    def start(self):
        self.manager.work()