# pylint: disable=attribute-defined-outside-init
from __future__ import annotations  # type: ignore

from setup.services_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.cdc import config
from src.cdc.adapters import repositories, views


class UnitOfWorkCdc(SqlAlchemyUnitOfWork):
    def __init__(self, session_factory=config.DEFAULT_SESSION_FACTORY):
        super().__init__(session_factory)

    def _enter(self):
        self.persons = repositories.PersonRepository(self.session)
        self.query_status = repositories.QueryStatusRepository(self.session)
        self.prospecto = repositories.ProspectoRepository(self.session)
        self.view_consult = views.ConsultasCDCView(self.session)
