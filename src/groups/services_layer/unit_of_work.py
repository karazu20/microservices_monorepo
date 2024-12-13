# pylint: disable=attribute-defined-outside-init
from __future__ import annotations  # type: ignore

from setup.services_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.groups import config
from src.groups.adapters import repositories, views


class UnitOfWorkGroups(SqlAlchemyUnitOfWork):
    def __init__(self, session_factory=config.DEFAULT_SESSION_FACTORY):
        super().__init__(session_factory)

    def _enter(self):
        self.view_grupo = views.GrupoView(self.session)
        self.groups = repositories.GroupRepository(self.session)
