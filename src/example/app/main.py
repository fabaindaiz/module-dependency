import time
from example.app import AppEnvironment
from example.plugin.manager import Manager

class MainApplication(AppEnvironment):
    manager = Manager.provided()
    manager.work()
    
    def loop(self):
        while True:
            time.sleep(1)