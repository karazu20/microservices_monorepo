from setup import inject
from src.sepomex.adapters import orm
from src.sepomex.services_layer import handlers
from src.sepomex.services_layer.unit_of_work import UnitOfWorkSepomex

broker = inject.start_broker(handlers=handlers, orm=orm, uow=UnitOfWorkSepomex())
