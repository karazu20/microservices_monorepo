from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import TYPE_CHECKING

from mambupy.api.mambuloan import MambuLoan
from mambupy.orm.schema_mambu import LoanAccount as ORMLoanAccount

from setup.adapters.mambu_models.model import EntityMambu, Mode, reloaded_attrs

if TYPE_CHECKING:

    from setup.adapters.mambu_models import (
        Branches,
        Centres,
        Comments,
        DisbursementsDetails,
        Groups,
        Installments,
        Products,
        Users,
    )

STATES_VALID_TO_APPROVAL = ["PENDING_APPROVAL"]
STATES_VALID_TO_DISBURSE = ["APPROVED"]


@dataclass(repr=False)
class Loans(EntityMambu):

    _model_rest = MambuLoan
    _model_orm = ORMLoanAccount

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Loans), mode, **kwargs)

    account_holder_type: str = field(
        metadata={
            "mambu_source": "accountHolderType",
            "read_only": False,
            "is_required": False,
        }
    )
    account_holder_key: str = field(
        metadata={
            "mambu_source": "accountHolderKey",
            "read_only": False,
            "is_required": False,
        }
    )

    approved_date: datetime = field(
        metadata={
            "mambu_source": "approvedDate",
            "read_only": False,
            "is_required": False,
        }
    )
    activation_transaction_key: str = field(
        metadata={
            "mambu_source": "activationTransactionKey",
            "read_only": False,
            "is_required": False,
        }
    )
    closed_date: datetime = field(
        metadata={"mambu_source": "closedDate", "read_only": False, "is_required": False}
    )
    last_account_appraisal_date: datetime = field(
        metadata={
            "mambu_source": "lastAccountAppraisalDate",
            "read_only": False,
            "is_required": False,
        }
    )
    account_state: str = field(
        metadata={
            "mambu_source": "accountState",
            "read_only": False,
            "is_required": False,
        }
    )
    account_sub_state: str = field(
        metadata={
            "mambu_source": "accountSubState",
            "read_only": False,
            "is_required": False,
        }
    )
    product_type_key: str = field(
        metadata={
            "mambu_source": "productTypeKey",
            "read_only": False,
            "is_required": False,
        }
    )
    loan_name: str = field(
        metadata={"mambu_source": "loanName", "read_only": False, "is_required": False}
    )
    loan_amount: float = field(
        metadata={"mambu_source": "loanAmount", "read_only": False, "is_required": False}
    )
    payment_method: str = field(
        metadata={
            "mambu_source": "paymentMethod",
            "read_only": False,
            "is_required": False,
        }
    )
    assigned_user_key: str = field(
        metadata={
            "mambu_source": "assignedUserKey",
            "read_only": False,
            "is_required": False,
        }
    )
    assigned_branch_key: str = field(
        metadata={
            "mambu_source": "assignedBranchKey",
            "read_only": False,
            "is_required": False,
        }
    )
    assigned_centre_key: str = field(
        metadata={
            "mambu_source": "assignedCentreKey",
            "read_only": False,
            "is_required": False,
        }
    )
    accrued_interest: int = field(
        metadata={
            "mambu_source": "accruedInterest",
            "read_only": False,
            "is_required": False,
        }
    )
    interest_from_arrears_accrued: int = field(
        metadata={
            "mambu_source": "interestFromArrearsAccrued",
            "read_only": False,
            "is_required": False,
        }
    )
    last_interest_applied_date: datetime = field(
        metadata={
            "mambu_source": "lastInterestAppliedDate",
            "read_only": False,
            "is_required": False,
        }
    )
    accrued_penalty: int = field(
        metadata={
            "mambu_source": "accruedPenalty",
            "read_only": False,
            "is_required": False,
        }
    )
    allow_offset: bool = field(
        metadata={"mambu_source": "allowOffset", "read_only": False, "is_required": False}
    )
    arrears_tolerance_period: int = field(
        metadata={
            "mambu_source": "arrearsTolerancePeriod",
            "read_only": False,
            "is_required": False,
        }
    )
    account_arrears_settings: dict = field(
        metadata={
            "mambu_source": "accountArrearsSettings",
            "read_only": False,
            "is_required": False,
        }
    )
    late_payments_recalculation_method: str = field(
        metadata={
            "mambu_source": "latePaymentsRecalculationMethod",
            "read_only": False,
            "is_required": False,
        }
    )
    balances: dict = field(
        metadata={"mambu_source": "balances", "read_only": False, "is_required": False}
    )
    disbursement_details: DisbursementsDetails = field(
        metadata={
            "mambu_source": "disbursementDetails",
            "is_vo": True,
            "read_only": False,
            "is_required": False,
            "model": "DisbursementsDetails",
        }
    )
    prepayment_settings: dict = field(
        metadata={
            "mambu_source": "prepaymentSettings",
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
    schedule_settings: dict = field(
        metadata={
            "mambu_source": "scheduleSettings",
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
    assets: list = field(
        metadata={"mambu_source": "assets", "read_only": False, "is_required": False}
    )
    guarantors: list = field(
        metadata={"mambu_source": "guarantors", "read_only": False, "is_required": False}
    )
    funding_sources: list = field(
        metadata={
            "mambu_source": "fundingSources",
            "read_only": False,
            "is_required": False,
        }
    )
    tranches: list = field(
        metadata={"mambu_source": "tranches", "read_only": False, "is_required": False}
    )
    future_payments_acceptance: str = field(
        metadata={
            "mambu_source": "futurePaymentsAcceptance",
            "read_only": False,
            "is_required": False,
        }
    )
    currency: dict = field(
        metadata={"mambu_source": "currency", "read_only": False, "is_required": False}
    )
    planned_installment_fees: list = field(
        metadata={
            "mambu_source": "plannedInstallmentFees",
            "read_only": False,
            "is_required": False,
        }
    )
    autorizacionoperativa_loan: dict = field(
        metadata={
            "mambu_source": "_autorizacionoperativa_loan",
            "read_only": False,
            "is_required": False,
        }
    )
    controlderiesgo_loan: dict = field(
        metadata={
            "mambu_source": "_controlderiesgo_loan",
            "read_only": False,
            "is_required": False,
        }
    )
    cuentasactivas_loan: dict = field(
        metadata={
            "mambu_source": "_cuentasactivas_loan",
            "read_only": False,
            "is_required": False,
        }
    )
    customfields_loan: dict = field(
        metadata={
            "mambu_source": "_customfields_loan",
            "read_only": False,
            "is_required": False,
        }
    )
    integrantes_loan: list[dict] = field(
        metadata={
            "mambu_source": "_integrantes_loan",
            "read_only": False,
            "is_required": False,
        }
    )
    autopmenu: Users = field(
        metadata={
            "mambu_source": "autopmenu",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_autorizacionoperativa_loan/autopmenu",
            "model": "Users",
        }
    )
    intgpomenu: Users = field(
        metadata={
            "mambu_source": "intgpomenu",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_autorizacionoperativa_loan/intgpomenu",
            "model": "Users",
        }
    )
    autlegmenu: Users = field(
        metadata={
            "mambu_source": "autlegmenu",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_autorizacionoperativa_loan/autlegmenu",
            "model": "Users",
        }
    )
    renovacion_loan_accounts: int = field(
        metadata={
            "mambu_source": "Renovacion_Loan_Accounts",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_autorizacionoperativa_loan/Renovacion_Loan_Accounts",
        }
    )
    generalidades_loan_accounts: int = field(
        metadata={
            "mambu_source": "Generalidades_Loan_Accounts",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_autorizacionoperativa_loan/Generalidades_Loan_Accounts",
        }
    )
    observaciones_expediente: bool = field(
        metadata={
            "mambu_source": "observaciones_expediente",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_controlderiesgo_loan/observaciones_expediente",
        }
    )
    integrantes_cdc: bool = field(
        metadata={
            "mambu_source": "integrantes_CdC",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_controlderiesgo_loan/integrantes_CdC",
        }
    )
    grupo_se_reune: bool = field(
        metadata={
            "mambu_source": "grupo_se_reune",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_controlderiesgo_loan/grupo_se_reune",
        }
    )
    restricciones_fam_dom_dist: bool = field(
        metadata={
            "mambu_source": "restricciones_fam_dom_dist",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_controlderiesgo_loan/restricciones_fam_dom_dist",
        }
    )
    num_observaciones: int = field(
        metadata={
            "mambu_source": "num_observaciones",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_controlderiesgo_loan/num_observaciones",
        }
    )
    fondeador: str = field(
        metadata={
            "mambu_source": "fondeador",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_cuentasactivas_loan/fondeador",
        }
    )
    ciclo: int = field(
        metadata={
            "mambu_source": "Ciclo",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_loan/Ciclo",
        }
    )
    dia_de_pago_loan_accounts: str = field(
        metadata={
            "mambu_source": "Dia_de_pago_Loan_Accounts",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_loan/Dia_de_pago_Loan_Accounts",
        }
    )
    fecha_de_la_primer_reunion_loan: str = field(
        metadata={
            "mambu_source": "Fecha_de_la_primer_reunion_Loan_",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_loan/Fecha_de_la_primer_reunion_Loan_",
        }
    )
    num_de_miembros_loan_accounts: int = field(
        metadata={
            "mambu_source": "Num_de_miembros_Loan_Accounts",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_loan/Num_de_miembros_Loan_Accounts",
        }
    )
    numero_desembolsos: int = field(
        metadata={
            "mambu_source": "numero_desembolsos",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_loan/numero_desembolsos",
        }
    )
    numero_ya_desembolsado: int = field(
        metadata={
            "mambu_source": "numero_ya_desembolsado",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_loan/numero_ya_desembolsado",
        }
    )
    montoanterior_0: int = field(
        metadata={
            "mambu_source": "montoanterior_0",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/0/montoanterior",
        }
    )
    monto_0: int = field(
        metadata={
            "mambu_source": "monto_0",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/0/monto",
        }
    )
    integrante_0: str = field(
        metadata={
            "mambu_source": "integrante_0",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/0/integrante",
        }
    )
    montoanterior_1: int = field(
        metadata={
            "mambu_source": "montoanterior_1",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/1/montoanterior",
        }
    )
    monto_1: int = field(
        metadata={
            "mambu_source": "monto_1",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/1/monto",
        }
    )
    integrante_1: str = field(
        metadata={
            "mambu_source": "integrante_1",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/1/integrante",
        }
    )
    montoanterior_2: int = field(
        metadata={
            "mambu_source": "montoanterior_2",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/2/montoanterior",
        }
    )
    monto_2: int = field(
        metadata={
            "mambu_source": "monto_2",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/2/monto",
        }
    )
    integrante_2: str = field(
        metadata={
            "mambu_source": "integrante_2",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/2/integrante",
        }
    )
    montoanterior_3: int = field(
        metadata={
            "mambu_source": "montoanterior_3",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/3/montoanterior",
        }
    )
    monto_3: int = field(
        metadata={
            "mambu_source": "monto_3",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/3/monto",
        }
    )
    integrante_3: str = field(
        metadata={
            "mambu_source": "integrante_3",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/3/integrante",
        }
    )
    montoanterior_4: int = field(
        metadata={
            "mambu_source": "montoanterior_4",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/4/montoanterior",
        }
    )
    monto_4: int = field(
        metadata={
            "mambu_source": "monto_4",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/4/monto",
        }
    )
    integrante_4: str = field(
        metadata={
            "mambu_source": "integrante_4",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/4/integrante",
        }
    )
    montoanterior_5: int = field(
        metadata={
            "mambu_source": "montoanterior_5",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/5/montoanterior",
        }
    )
    monto_5: int = field(
        metadata={
            "mambu_source": "monto_5",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/5/monto",
        }
    )
    integrante_5: str = field(
        metadata={
            "mambu_source": "integrante_5",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/5/integrante",
        }
    )
    montoanterior_6: int = field(
        metadata={
            "mambu_source": "montoanterior_6",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/6/montoanterior",
        }
    )
    monto_6: int = field(
        metadata={
            "mambu_source": "monto_6",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/6/monto",
        }
    )
    integrante_6: str = field(
        metadata={
            "mambu_source": "integrante_6",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/6/integrante",
        }
    )
    montoanterior_7: int = field(
        metadata={
            "mambu_source": "montoanterior_7",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/7/montoanterior",
        }
    )
    monto_7: int = field(
        metadata={
            "mambu_source": "monto_7",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/7/monto",
        }
    )
    integrante_7: str = field(
        metadata={
            "mambu_source": "integrante_7",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_integrantes_loan/7/integrante",
        }
    )
    assigned_user: Users = field(
        metadata={
            "mambu_source": "assignedUser",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Users",
        }
    )
    assigned_branch: Branches = field(
        metadata={
            "mambu_source": "assignedBranch",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Branches",
        }
    )
    assigned_centre: Centres = field(
        metadata={
            "mambu_source": "assignedCentre",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Centres",
        }
    )
    product_type: Products = field(
        metadata={
            "mambu_source": "productType",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Products",
        }
    )
    account_holder: Groups = field(
        metadata={
            "mambu_source": "accountHolder",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Groups",
        }
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

    installments: list[Installments] = field(
        metadata={
            "mambu_source": "schedule",
            "is_vo": True,
            "is_many": True,
            "read_only": False,
            "is_required": False,
            "lazy_from_method": "get_schedule",
            "model": "Installments",
        }
    )
    creation_date: datetime = field(
        metadata={
            "mambu_source": "creationDate",
            "read_only": False,
            "is_required": False,
        }
    )
    original_account_key: datetime = field(
        metadata={
            "mambu_source": "originalAccountKey",
            "read_only": False,
            "is_required": False,
        }
    )
    sub_status_web: str = field(
        metadata={
            "mambu_source": "sub_status_web",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_loan/sub_status_web",
        }
    )

    def write(self, data: dict):
        if "account_state" in data:
            try:
                data["notes"]
            except KeyError:
                data["notes"] = "Updated via API"
            self.update_state(data["account_state"], data["notes"])
            del data["account_state"]
            del data["notes"]
        return super().write(data)

    @reloaded_attrs(attrs=["account_state"])
    def update_state(self, state: str, notes: str):
        if self._mode == Mode.REST:
            return self._instance_mambu.set_state(action=state, notes=notes)
        else:
            raise Exception("ORM mode does not support write operations.")

    @reloaded_attrs(attrs=["account_state"])
    def approve(self, notes: str):
        if self._mode == Mode.REST:
            if self.account_state in STATES_VALID_TO_APPROVAL:
                return self._instance_mambu.approve(notes=notes)
            else:
                raise Exception(
                    f"Loan '{self.id}' with state '{self.account_state}', is a state not valid to approve"
                )
        else:
            raise Exception("ORM mode does not support write operations.")

    @reloaded_attrs(attrs=["account_state"])
    def disburse(
        self,
        notes: str,
        first_repayment_date: datetime = None,
        disbursement_date: datetime = None,
    ):
        if self._mode == Mode.REST:
            if self.account_state in STATES_VALID_TO_DISBURSE:
                return self._instance_mambu.disburse(
                    notes=notes,
                    firstRepaymentDate=first_repayment_date,
                    disbursementDate=disbursement_date,
                )
            else:
                raise Exception(
                    f"Loan '{self.id}' with state '{self.account_state}', is a state not valid to disburse"
                )
        else:
            raise Exception("ORM mode does not support write operations.")

    @property
    def full_name_ce(self):
        if self.assigned_user:
            return self.assigned_user.first_name + " " + self.assigned_user.last_name

        return ""

    @property
    def tribu(self):
        if self.assigned_centre:
            return self.assigned_centre.name
        return ""

    @property
    def community_center(self):
        if self.assigned_branch:
            return self.assigned_branch.name
        return ""

    @property
    def transactions(self):
        from setup.adapters.mambu_models.transactions import Transactions

        if self.encoded_key:
            return Transactions.search([("parent_account_key", "=", self.encoded_key)])
        return []

    @classmethod
    def search_by_tribu(cls, centre_id: str, limit: int, offset: int):
        instances_mambu = cls._model_rest.get_all(
            filters={"centreId": centre_id},
            limit=limit,
            offset=offset,
        )
        return [cls.get(instance_mambu.id) for instance_mambu in instances_mambu]
