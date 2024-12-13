from setup import inject
from src.groups.adapters import orm
from src.groups.services_layer import handlers
from src.groups.services_layer.unit_of_work import UnitOfWorkGroups

broker = inject.start_broker(handlers=handlers, orm=orm, uow=UnitOfWorkGroups())
