from setup import inject
from src.cdc.adapters import orm
from src.cdc.services_layer import handlers
from src.cdc.services_layer.unit_of_work import UnitOfWorkCdc

broker = inject.start_broker(handlers=handlers, orm=orm, uow=UnitOfWorkCdc())
