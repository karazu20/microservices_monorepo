from setup import inject
from src.mambu.services_layer import handlers

broker = inject.start_broker(handlers=handlers, orm=[], uow=[])  # type: ignore
