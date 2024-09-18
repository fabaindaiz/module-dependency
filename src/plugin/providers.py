def get():
    from src.plugin.client.type1.container import Type1ClientProvider
    from src.plugin.manager.type1.container import Type1ManagerProvider
    return [
        Type1ClientProvider,
        Type1ManagerProvider,
    ]