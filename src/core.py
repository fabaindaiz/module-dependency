
class Component:
    pass

from dependency_injector import containers, providers

class Provider:
    pass

def provider(cls = None, /, *,
             name: str = None,
             depends: list[Component] = None,
             config: Component = None):
    def wrap(cls):
        return cls

    if cls is None:
        return wrap
    
    return wrap(cls)


class Container:
    pass

class Module:
    pass

def module(cls = None, /, *,
           declaration: list[Component] = None,
           imports: list[Component] = None):
    def wrap(cls):
        return cls

    if cls is None:
        return wrap
    
    return wrap(cls)