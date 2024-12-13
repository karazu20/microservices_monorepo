from typing import Callable, Dict, Type  # isort:skip

from setup import domain  # type: ignore
from setup.adapters import podemos_mambu
from src.transactions.config import TYPE_TRANSACTION
from src.transactions.domain import queries


def get_transactions(
    query: queries.GetTransactions,
    mambu: podemos_mambu.PodemosMambu,
):
    loan = mambu.loans.get(id=query.loan_id)
    transactions = loan.transactions

    array_transactions = []
    for value in transactions:

        try:
            principal_amount = value.account_balances["principalBalance"]
        except Exception:
            principal_amount = 0

        try:
            total_balance = value.account_balances["totalBalance"]
        except Exception:
            total_balance = 0

        try:
            arrears_position = value.account_balances["arrearsPosition"]
        except Exception:
            arrears_position = 0

        array_transactions.append(
            {
                "id": value.id,
                "value_date": value.value_date,
                "user": value.user_key,
                "type": TYPE_TRANSACTION[value.type_transaction],
                "amount": value.amount,
                "principal_amount": principal_amount,
                "total_balance": total_balance,
                "arrears_position": arrears_position,
            }
        )

    return array_transactions


def get_installments(
    query: queries.GetInstallments,
    mambu: podemos_mambu.PodemosMambu,
):
    loan = mambu.loans.get(id=query.loan_id)
    installments = loan.installments

    return [
        {
            "parent_account_key": value.parent_account_key,
            "number": value.number,
            "due_date": value.due_date,
            "last_paid_date": value.last_paid_date,
            "repaid_date": value.repaid_date,
            "state": value.state,
            "is_payment_holiday": value.is_payment_holiday,
            "principal": value.principal,
            "interest": value.interest,
            "fee": value.fee,
            "penalty": value.penalty,
        }
        for value in installments
    ]


QUERY_HANDLERS = {
    queries.GetTransactions: get_transactions,
    queries.GetInstallments: get_installments,
}  # type: Dict[Type[domain.Query], Callable]


COMMAND_HANDLERS = {}  # type: ignore


EVENT_HANDLERS = {}  # type: ignore
