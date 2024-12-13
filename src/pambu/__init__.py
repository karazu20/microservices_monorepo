from setup import inject
from src.pambu.adapters import orm
from src.pambu.services_layer import handlers
from src.pambu.services_layer.unit_of_work import UnitOfWorkPambu

broker = inject.start_broker(handlers=handlers, orm=orm, uow=UnitOfWorkPambu())
