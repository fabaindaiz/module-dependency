from dependency.core.injection.loader import InjectionLoader
from example.app.main import MainApplication

def test_main():
    app = MainApplication()
    loader: InjectionLoader = app.loader
    assert loader is not None
    assert len(loader.resolved) == len(loader.providers)