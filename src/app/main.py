from src.manager.container import ManagerMixin
from src.app import AppEnvironment

class MainApplication(AppEnvironment, ManagerMixin):
    def load(self):
        self.manager.load()

    def start(self):
        self.manager.work()