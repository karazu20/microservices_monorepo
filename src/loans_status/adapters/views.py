from typing import Optional

from setup.adapters.data import SQLView
from src.loans_status.domain import queries
from src.loans_status.domain.models import LoanStatus


class LoanStatusView(SQLView):
    def _search(
        self,
        qry: queries.GetLoanStatus,
    ) -> Optional[list]:

        if qry.id_mambu and qry.estatus:
            return (
                self.session.query(LoanStatus)
                .filter(LoanStatus.estatus.in_(qry.estatus))  # type: ignore
                .filter(LoanStatus.id_mambu.in_(qry.id_mambu))  # type: ignore
                .all()
            )
        elif qry.id_mambu:
            return (
                self.session.query(LoanStatus)
                .filter(LoanStatus.id_mambu.in_(qry.id_mambu))  # type: ignore
                .all()
            )
        elif qry.estatus:
            return (
                self.session.query(LoanStatus)
                .filter(LoanStatus.estatus.in_(qry.estatus))  # type: ignore
                .all()
            )
        else:
            return self.session.query(LoanStatus).all()
