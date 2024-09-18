import time
from app import AppEnvironment
from plugin.manager import Manager

class MainApplication(AppEnvironment):
    manager = Manager()
    manager.work()
    
    def loop(self):
        while True:
            time.sleep(1)