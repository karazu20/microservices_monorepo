from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from datetime import datetime

from mambupy.api.vos import MambuDisbursementDetails

from setup.adapters.mambu_models.model import Mode, VOMambu


@dataclass(repr=False)
class DisbursementsDetails(VOMambu):
    _model_rest = MambuDisbursementDetails

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(DisbursementsDetails), mode, **kwargs)

    expected_disbursement_date: datetime = field(
        metadata={
            "mambu_source": "expectedDisbursementDate",
            "read_only": False,
            "is_required": False,
        }
    )
    disbursement_date: datetime = field(
        metadata={
            "mambu_source": "disbursementDate",
            "read_only": False,
            "is_required": False,
        }
    )
    first_repayment_date: datetime = field(
        metadata={
            "mambu_source": "firstRepaymentDate",
            "read_only": False,
            "is_required": False,
        }
    )
    transaction_details: dict = field(
        metadata={
            "mambu_source": "transactionDetails",
            "read_only": False,
            "is_required": False,
        }
    )
    fees: list[dict] = field(
        metadata={"mambu_source": "fees", "read_only": False, "is_required": False}
    )
