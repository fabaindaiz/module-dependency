import time
from example.app import AppEnvironment

class MainApplication(AppEnvironment):
    
    def loop(self):
        while True:
            time.sleep(1)