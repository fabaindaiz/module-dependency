from dependency_injector.wiring import Provide

class Component:
    def __init__(self,
            base_cls,
        ):
        self.base_cls = base_cls
    
    @classmethod
    def inject_cls(cls):
        return cls

    def __repr__(self) -> str:
        return self.base_cls.__name__

def component(
        interface
    ) -> Component:
    def wrap(cls):
        class WrapComponent(Component):
            def __init__(self):
                super().__init__(
                    base_cls=interface.__class__)
            
            def __call__(self,
                    service = Provide[f"{interface.__class__.__name__}.service"]
                ) -> interface:
                return service
        return WrapComponent()
    return wrap