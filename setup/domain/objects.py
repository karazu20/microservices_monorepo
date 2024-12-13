class Model:
    pass


class EntityRoot(Model):
    pass


class Entity(Model):
    pass


class ValueObject(Model):
    pass


class Command:
    pass


class Query:
    pass


class Event:
    channel: str = NotImplemented
