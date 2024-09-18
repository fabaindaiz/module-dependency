def get():
    from plugin.client.type1 import Type1Client
    from plugin.manager.type1 import Type1Manager
    return [
        Type1Client,
        Type1Manager,
    ]