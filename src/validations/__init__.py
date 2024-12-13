from setup import inject
from src.validations.adapters import orm
from src.validations.services_layer import handlers
from src.validations.services_layer.unit_of_work import UnitOfWorkValidations

broker = inject.start_broker(handlers=handlers, orm=orm, uow=UnitOfWorkValidations())
