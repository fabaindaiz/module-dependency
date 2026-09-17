from dependency.library.graph import generate_graph
from example.app.main import MonitoringStation
from example.app.main.plugins import PLUGINS

if __name__ == "__main__":
    MonitoringStation()
    generate_graph(PLUGINS)
