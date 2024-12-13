from setup import inject
from src.storage.adapters import orm
from src.storage.services_layer import handlers
from src.storage.services_layer.unit_of_work import UnitOfWorkDocument

broker = inject.start_broker(handlers=handlers, orm=orm, uow=UnitOfWorkDocument())  # type: ignore
