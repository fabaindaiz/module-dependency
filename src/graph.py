from dependency.core.utils.graph import generate_graph
from example.app.main import MainApplication

if __name__ == "__main__":
    app = MainApplication()
    generate_graph(include_modules=True)
