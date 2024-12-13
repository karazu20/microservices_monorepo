# pylint: disable=attribute-defined-outside-init
from __future__ import annotations  # type: ignore

from setup.services_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.loans_status import config
from src.loans_status.adapters import repositories, views


class UnitOfWorkLoansStatus(SqlAlchemyUnitOfWork):
    def __init__(self, session_factory=config.DEFAULT_SESSION_FACTORY):
        super().__init__(session_factory)

    def _enter(self):
        self.loan_status = repositories.LoanStatusRepository(self.session)
        self.view_loan_status = views.LoanStatusView(self.session)
