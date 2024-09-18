def get():
    from src.services.factory.type1.container import Type1FactoryServiceProvider
    from src.services.singleton.type1.container import Type1SingletonServiceProvider
    return [
        Type1FactoryServiceProvider,
        Type1SingletonServiceProvider,
    ]