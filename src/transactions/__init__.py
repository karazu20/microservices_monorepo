from setup import inject
from src.transactions.services_layer import handlers

broker = inject.start_broker(handlers=handlers, orm=[], uow=[])  # type: ignore
