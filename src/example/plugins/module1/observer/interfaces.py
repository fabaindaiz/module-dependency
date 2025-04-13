from library.mixins.observer import EventContext, EventSubscriber

class ObserverEventContext(EventContext):
    pass

class EventProductCreated(ObserverEventContext):
    def __init__(self, product: str):
        self.product = product

class EventProductOperation(ObserverEventContext):
    def __init__(self, product: str, operation: str):
        self.product = product
        self.operation = operation

class EventProductCreatedSubscriber(EventSubscriber[EventProductCreated]):
    pass

class EventProductOperationSubscriber(EventSubscriber[EventProductOperation]):
    pass