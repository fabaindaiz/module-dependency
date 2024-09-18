def get():
    from services.factory.type1 import Type1Factory
    from services.singleton.type1 import Type1Singleton
    return [
        Type1Factory,
        Type1Singleton,
    ]