from setup import inject
from src.nip.adapters import orm
from src.nip.services_layer import handlers
from src.nip.services_layer.unit_of_work import UnitOfWorkNip

broker = inject.start_broker(handlers=handlers, orm=orm, uow=UnitOfWorkNip())
