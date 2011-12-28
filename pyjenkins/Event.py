from pyjenkins.interfaces import IEvent

class Event(IEvent):

    def __init__(self):
        self.handlers = set()

    def register(self, handler):
        self.handlers.add(handler)

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)


