# pylint: disable=attribute-defined-outside-init
from __future__ import annotations  # type: ignore

from setup.services_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.sepomex import config
from src.sepomex.adapters import repositories, views


class UnitOfWorkSepomex(SqlAlchemyUnitOfWork):
    def __init__(self, session_factory=config.DEFAULT_SESSION_FACTORY):
        super().__init__(session_factory)

    def _enter(self):
        self.estados = repositories.EstadoRepository(self.session)
        self.municipios = repositories.MunicipioRepository(self.session)
        self.view_postal_code = views.PostalCodeView(self.session)
