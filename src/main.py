import logging
from example.app.main import MonitoringStation

logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")

if __name__ == "__main__":
    station = MonitoringStation()
    station.main_loop()
