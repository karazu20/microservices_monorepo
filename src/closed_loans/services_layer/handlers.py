from typing import Callable, Dict, Type  # isort:skip


from setup import domain  # type: ignore
from setup.adapters import podemos_mambu
from src.closed_loans.domain import queries

SUB_STATE_LABEL = {
    "REPAID": "Todas las Obligaciones Cumplidas",
    "RESCHEDULED": "Renegociada",
    "REFINANCED": "Refinanciada",
    "LOCKED": "Bloqueada",
    "WITHDRAWN": "Retirado",
    "WRITTEN_OFF": "Cancelada",
}


def get_closed_loans(
    query: queries.GetClosedLoans,
    mambu: podemos_mambu.PodemosMambu,
):
    group = mambu.groups.get(id=query.group_id)

    return [
        {
            "id": value.id,
            "loan_name": value.loan_name,
            "amount": value.loan_amount,
            "interest_settings": value.interest_settings,
            "closed_date": value.closed_date,
            "account_state": value.account_state,
            "account_sub_state": value.account_sub_state,
            "account_sub_state_label": SUB_STATE_LABEL[value.account_sub_state],
        }
        for value in group.previous_loans
    ]


QUERY_HANDLERS = {
    queries.GetClosedLoans: get_closed_loans,
}  # type: Dict[Type[domain.Query], Callable]


COMMAND_HANDLERS = {}  # type: ignore


EVENT_HANDLERS = {}  # type: ignore
