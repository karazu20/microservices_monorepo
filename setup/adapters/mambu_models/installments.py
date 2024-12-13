from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from datetime import datetime

from mambupy.api.entities import MambuInstallment

from setup.adapters.mambu_models.model import Mode, VOMambu


@dataclass(repr=False)
class Installments(VOMambu):
    _model_rest = MambuInstallment

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Installments), mode, **kwargs)

    parent_account_key: str = field(
        metadata={
            "mambu_source": "parentAccountKey",
            "read_only": False,
            "is_required": False,
        }
    )

    number: int = field(
        metadata={
            "mambu_source": "number",
            "read_only": False,
            "is_required": False,
        }
    )

    due_date: datetime = field(
        metadata={
            "mambu_source": "dueDate",
            "read_only": False,
            "is_required": False,
        }
    )

    last_paid_date: datetime = field(
        metadata={
            "mambu_source": "lastPaidDate",
            "read_only": False,
            "is_required": False,
        }
    )

    repaid_date: datetime = field(
        metadata={
            "mambu_source": "repaidDate",
            "read_only": False,
            "is_required": False,
        }
    )

    state: str = field(
        metadata={
            "mambu_source": "state",
            "read_only": False,
            "is_required": False,
        }
    )

    is_payment_holiday: bool = field(
        metadata={
            "mambu_source": "isPaymentHoliday",
            "read_only": False,
            "is_required": False,
        }
    )

    principal: dict = field(
        metadata={"mambu_source": "principal", "read_only": False, "is_required": False}
    )

    interest: dict = field(
        metadata={"mambu_source": "interest", "read_only": False, "is_required": False}
    )

    fee: dict = field(
        metadata={"mambu_source": "fee", "read_only": False, "is_required": False}
    )

    penalty: dict = field(
        metadata={"mambu_source": "penalty", "read_only": False, "is_required": False}
    )
