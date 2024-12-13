from setup import inject
from src.loans_status.adapters import orm
from src.loans_status.services_layer import handlers
from src.loans_status.services_layer.unit_of_work import UnitOfWorkLoansStatus

broker = inject.start_broker(handlers=handlers, orm=orm, uow=UnitOfWorkLoansStatus())
