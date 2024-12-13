from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from datetime import datetime

from mambupy.api.mambutransaction import MambuTransaction
from mambupy.orm.schema_mambu import LoanTransaction as ORMLoanTransaction

from setup.adapters.mambu_models.model import EntityMambu, Mode


@dataclass(repr=False)
class Transactions(EntityMambu):

    _model_rest = MambuTransaction
    _model_orm = ORMLoanTransaction

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Transactions), mode, **kwargs)

    value_date: datetime = field(
        metadata={"mambu_source": "valueDate", "read_only": False, "is_required": False}
    )
    notes: str = field(
        metadata={"mambu_source": "notes", "read_only": False, "is_required": False}
    )
    parent_account_key: str = field(
        metadata={
            "mambu_source": "parentAccountKey",
            "read_only": False,
            "is_required": False,
        }
    )
    type_transaction: str = field(
        metadata={"mambu_source": "type", "read_only": False, "is_required": False}
    )
    amount: float = field(
        metadata={"mambu_source": "amount", "read_only": False, "is_required": False}
    )
    affected_amounts: dict = field(
        metadata={
            "mambu_source": "affectedAmounts",
            "read_only": False,
            "is_required": False,
        }
    )
    taxes: dict = field(
        metadata={"mambu_source": "taxes", "read_only": False, "is_required": False}
    )
    account_balances: dict = field(
        metadata={
            "mambu_source": "accountBalances",
            "read_only": False,
            "is_required": False,
        }
    )
    user_key: str = field(
        metadata={"mambu_source": "userKey", "read_only": False, "is_required": False}
    )
    branch_key: str = field(
        metadata={"mambu_source": "branchKey", "read_only": False, "is_required": False}
    )
    centre_key: str = field(
        metadata={"mambu_source": "centreKey", "read_only": False, "is_required": False}
    )
    terms: dict = field(
        metadata={"mambu_source": "terms", "read_only": False, "is_required": False}
    )
    transaction_details: dict = field(
        metadata={
            "mambu_source": "transactionDetails",
            "read_only": False,
            "is_required": False,
        }
    )
    fees: list = field(
        metadata={"mambu_source": "fees", "read_only": False, "is_required": False}
    )
    detalles_transaccion: dict = field(
        metadata={
            "mambu_source": "_detalles_transaccion",
            "read_only": False,
            "is_required": False,
        }
    )
    informacion_bancaria: str = field(
        metadata={
            "mambu_source": "informacion_bancaria",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_detalles_transaccion/informacion_bancaria",
        }
    )
