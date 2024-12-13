from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING

from mambupy.api.mambugroup import MambuGroup
from mambupy.orm.schema_mambu import Group as ORMGroup

from setup.adapters.mambu_models.model import EntityMambu, Mode

if TYPE_CHECKING:
    from setup.adapters.mambu_models import (
        Addresses,
        Branches,
        Centres,
        Comments,
        GroupMembers,
        Users,
    )

STATES_PREVIEWS_LOANS = ["CLOSED"]


@dataclass(repr=False)
class Groups(EntityMambu):
    _model_rest = MambuGroup
    _model_orm = ORMGroup

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Groups), mode, **kwargs)

    group_name: str = field(
        metadata={"mambu_source": "groupName", "read_only": False, "is_required": False}
    )
    notes: str = field(
        metadata={"mambu_source": "notes", "read_only": False, "is_required": False}
    )
    assigned_branch_key: str = field(
        metadata={
            "mambu_source": "assignedBranchKey",
            "read_only": False,
            "is_required": False,
        }
    )
    loan_cycle: int = field(
        metadata={"mambu_source": "loanCycle", "read_only": False, "is_required": False}
    )
    email_address: str = field(
        metadata={
            "mambu_source": "emailAddress",
            "read_only": False,
            "is_required": False,
        }
    )
    mobile_phone: str = field(
        metadata={"mambu_source": "mobilePhone", "read_only": False, "is_required": False}
    )
    home_phone: str = field(
        metadata={"mambu_source": "homePhone", "read_only": False, "is_required": False}
    )
    preferred_language: str = field(
        metadata={
            "mambu_source": "preferredLanguage",
            "read_only": False,
            "is_required": False,
        }
    )
    group_role_key: str = field(
        metadata={
            "mambu_source": "groupRoleKey",
            "read_only": False,
            "is_required": False,
        }
    )
    addresses: list[Addresses] = field(
        metadata={
            "mambu_source": "addresses",
            "is_vo": True,
            "is_many": True,
            "read_only": False,
            "is_required": False,
            "model": "Addresses",
        }
    )
    group_members: list[GroupMembers] = field(
        metadata={
            "mambu_source": "groupMembers",
            "is_vo": True,
            "is_many": True,
            "read_only": False,
            "is_required": False,
            "model": "GroupMembers",
        }
    )
    customfields_grupo: dict = field(
        metadata={
            "mambu_source": "_customfields_grupo",
            "read_only": False,
            "is_required": False,
        }
    )
    dia_de_reunion_groups: str = field(
        metadata={
            "mambu_source": "Dia_de_reunion_Groups",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_grupo/Dia_de_reunion_Groups",
        }
    )
    referencia_de_ubicacion_groups: str = field(
        metadata={
            "mambu_source": "Referencia_de_ubicacion_Groups",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_grupo/Referencia_de_ubicacion_Groups",
        }
    )
    nivel_groups: int = field(
        metadata={
            "mambu_source": "Nivel_Groups",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_grupo/Nivel_Groups",
        }
    )
    calificacion_groups: int = field(
        metadata={
            "mambu_source": "Calificacion_Groups",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_grupo/Calificacion_Groups",
        }
    )
    hora_de_reunion_groups: str = field(
        metadata={
            "mambu_source": "Hora_de_reunion_Groups",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_grupo/Hora_de_reunion_Groups",
        }
    )
    ciclo_tipo_groups: str = field(
        metadata={
            "mambu_source": "Ciclo-Tipo_Groups",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_grupo/Ciclo-Tipo_Groups",
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
    riesgo_grupo: str = field(
        metadata={
            "mambu_source": "riesgo_grupo",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_riesgo_grupo/riesgo_grupo",
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
    assigned_centre: Centres = field(
        metadata={
            "mambu_source": "assignedCentre",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Centres",
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

    @property
    def full_name_ce(self):
        try:
            return self.assigned_user.first_name + " " + self.assigned_user.last_name
        except Exception:
            return ""

        return ""

    @property
    def tribu(self):
        try:
            return self.assigned_centre.name
        except Exception:
            return ""

        return ""

    @property
    def community_center(self):
        try:
            return self.assigned_branch.name
        except Exception:
            return ""

        return ""

    @property
    def members(self):
        return [member.client for member in self.group_members]

    @property
    def full_addresses(self):
        if self.addresses:
            return [
                address.line_1
                + " "
                + address.line_2
                + " "
                + address.city
                + " "
                + address.region
                + " "
                + str(address.postcode)
                + " "
                + address.country
                for address in self.addresses
            ]
        return []

    @property
    def loans(self):
        from setup.adapters.mambu_models.loans import Loans

        return Loans.search([("account_holder_key", "=", self.encoded_key)])

    @property
    def previous_loans(self):
        return [l for l in self.loans if l.account_state in STATES_PREVIEWS_LOANS]
