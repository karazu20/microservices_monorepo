from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING

from mambupy.api.mambuproduct import MambuProduct
from mambupy.orm import schema_orm as orm
from mambupy.orm.schema_mambu import LoanProduct as ORMLoanProduct

from setup.adapters.mambu_models.model import EntityMambu, MambuModel, Mode

if TYPE_CHECKING:
    from setup.adapters.mambu_models import Comments


@dataclass(repr=False)
class Products(EntityMambu):

    _model_rest = MambuProduct
    _model_orm = ORMLoanProduct

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Products), mode, **kwargs)

    name: str = field(
        metadata={"mambu_source": "name", "read_only": False, "is_required": False}
    )
    notes: str = field(
        metadata={"mambu_source": "notes", "read_only": False, "is_required": False}
    )
    type: str = field(
        metadata={"mambu_source": "type", "read_only": False, "is_required": False}
    )
    category: str = field(
        metadata={"mambu_source": "category", "read_only": False, "is_required": False}
    )
    state: str = field(
        metadata={"mambu_source": "state", "read_only": False, "is_required": False}
    )
    loan_amount_settings: dict = field(
        metadata={
            "mambu_source": "loanAmountSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    schedule_settings: dict = field(
        metadata={
            "mambu_source": "scheduleSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    payment_settings: dict = field(
        metadata={
            "mambu_source": "paymentSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    grace_period_settings: dict = field(
        metadata={
            "mambu_source": "gracePeriodSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    new_account_settings: dict = field(
        metadata={
            "mambu_source": "newAccountSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    interest_settings: dict = field(
        metadata={
            "mambu_source": "interestSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    penalty_settings: dict = field(
        metadata={
            "mambu_source": "penaltySettings",
            "read_only": False,
            "is_required": False,
        }
    )
    arrears_settings: dict = field(
        metadata={
            "mambu_source": "arrearsSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    fees_settings: dict = field(
        metadata={
            "mambu_source": "feesSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    accounting_settings: dict = field(
        metadata={
            "mambu_source": "accountingSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    account_link_settings: dict = field(
        metadata={
            "mambu_source": "accountLinkSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    tax_settings: dict = field(
        metadata={"mambu_source": "taxSettings", "read_only": False, "is_required": False}
    )
    internal_controls: dict = field(
        metadata={
            "mambu_source": "internalControls",
            "read_only": False,
            "is_required": False,
        }
    )
    security_settings: dict = field(
        metadata={
            "mambu_source": "securitySettings",
            "read_only": False,
            "is_required": False,
        }
    )
    credit_arrangement_settings: dict = field(
        metadata={
            "mambu_source": "creditArrangementSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    funding_settings: dict = field(
        metadata={
            "mambu_source": "fundingSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    availability_settings: dict = field(
        metadata={
            "mambu_source": "availabilitySettings",
            "read_only": False,
            "is_required": False,
        }
    )
    allow_custom_repayment_allocation: bool = field(
        metadata={
            "mambu_source": "allowCustomRepaymentAllocation",
            "read_only": False,
            "is_required": False,
        }
    )
    templates: list = field(
        metadata={"mambu_source": "templates", "read_only": False, "is_required": False}
    )
    currency: dict = field(
        metadata={"mambu_source": "currency", "read_only": False, "is_required": False}
    )
    comments: list[Comments] = field(
        metadata={
            "mambu_source": "_comments",
            "is_vo": True,
            "is_many": True,
            "read_only": False,
            "is_required": False,
            "lazy_from_method": "get_comments",
            "model": "Comments",
        }
    )

    @classmethod
    def get(cls, id, mode=Mode.REST) -> MambuModel:

        if mode == Mode.REST:
            instance_mambu = cls._model_rest.get(entid=id, get_entities=False)
        else:
            session = orm.Session()
            instance_mambu = session.query(cls._model_orm).filter_by(id=id).first()

        return cls(instance_mambu, mode)
