from setup.adapters.data import SQLRepository
from src.loans_status.domain.models import LoanStatus


class LoanStatusRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, LoanStatus)  # type: ignore
        self.loan_status = LoanStatus

    def _get(self, id_mambu) -> LoanStatus:
        return self.session.query(LoanStatus).filter_by(id_mambu=id_mambu).first()
