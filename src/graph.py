from dependency.library.graph import generate_graph
from example.app.main import MainApplication
from example.app.main.plugins import PLUGINS

if __name__ == "__main__":
    app = MainApplication()
    generate_graph(PLUGINS)
