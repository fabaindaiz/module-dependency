from example.app.main import MainApplication

def test_main():
    app = MainApplication()
    assert app.loader is not None