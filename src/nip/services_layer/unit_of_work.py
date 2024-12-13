# pylint: disable=attribute-defined-outside-init
from __future__ import annotations

from setup.services_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.nip import config
from src.nip.adapters import repositories


class UnitOfWorkNip(SqlAlchemyUnitOfWork):
    def __init__(self, session_factory=config.DEFAULT_SESSION_FACTORY):
        super().__init__(session_factory)

    def _enter(self):
        self.nips = repositories.NipRepository(self.session)
