from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING

from mambupy.api.mambubranch import MambuBranch
from mambupy.orm.schema_mambu import Branch as ORMBranch

from setup.adapters.mambu_models.model import EntityMambu, Mode

if TYPE_CHECKING:
    from setup.adapters.mambu_models import Addresses, Comments


@dataclass(repr=False)
class Branches(EntityMambu):
    _model_rest = MambuBranch
    _model_orm = ORMBranch

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Branches), mode, **kwargs)

    name: str = field(
        metadata={"mambu_source": "name", "read_only": False, "is_required": False}
    )
    state: str = field(
        metadata={"mambu_source": "state", "read_only": False, "is_required": False}
    )
    phone_number: str = field(
        metadata={"mambu_source": "phoneNumber", "read_only": False, "is_required": False}
    )
    email_address: str = field(
        metadata={
            "mambu_source": "emailAddress",
            "read_only": False,
            "is_required": False,
        }
    )
    notes: str = field(
        metadata={"mambu_source": "notes", "read_only": False, "is_required": False}
    )
    branch_holidays: list = field(
        metadata={
            "mambu_source": "branchHolidays",
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
    customfields_branch: dict = field(
        metadata={
            "mambu_source": "_customfields_branch",
            "read_only": False,
            "is_required": False,
        }
    )
    contactos_branch: list[dict] = field(
        metadata={
            "mambu_source": "_contactos_branch",
            "read_only": False,
            "is_required": False,
        }
    )
    branch_region_us: str = field(
        metadata={
            "mambu_source": "branch_region_us",
            "read_only": False,
            "is_required": False,
        }
    )
    contacto_0: str = field(
        metadata={"mambu_source": "contacto_0", "read_only": False, "is_required": False}
    )
    contacto_1: str = field(
        metadata={"mambu_source": "contacto_1", "read_only": False, "is_required": False}
    )
    contacto_2: str = field(
        metadata={"mambu_source": "contacto_2", "read_only": False, "is_required": False}
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
